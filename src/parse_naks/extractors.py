from abc import ABC, abstractmethod
from re import search, findall
from datetime import date
from typing import Generic

from lxml import html

from src.services.utils import str_to_date
from src.parse_naks.types import WelderData, Model, Link


"""
=======================================================================================================
Extractors
=======================================================================================================
"""


class IExtractor(ABC, Generic[Model]):

    @abstractmethod
    def extract(self, main_page: str, additional_pages: list[str]) -> list[Model]: ...


    @staticmethod
    def extract_links(welder_page: str) -> list[Link]:
        tree = html.fromstring(welder_page)
        links = tree.xpath("//tr[@bgcolor]/td[13]/a/@onclick")
        links = [search(r"/[\w]+/[\w]+/detail.php\?ID=[\w\W]+", link)[0].replace('"', '').split(",")[0] for link in links]

        links = [f"https://naks.ru{link}" for link in links]

        return links


class WelderDataExtractor(IExtractor):
    
    def extract(self, main_page: str, additional_pages: list[str]) -> list[WelderData]:
        result = []

        main_page_data = self._extract_data_from_welder_page(main_page)

        for page_index in range(len(additional_pages)):
            additional_page_data = self._extract_data_from_welder_certification_page(
                additional_pages[page_index]
            )

            data = main_page_data[page_index] | additional_page_data

            result.append(
                WelderData.model_validate(data)
            )

        return result


    def _extract_data_from_welder_page(self, welder_page: str) -> list[dict[str, str | date | None]]:
        result = []
        tree = html.fromstring(welder_page)

        trs = tree.xpath("//tr[@bgcolor]")

        for tr in trs:
            row_tree = html.fromstring(html.tostring(tr))
            name = self._get_value(row_tree, "//tr[@bgcolor]/td[1]/text()")
            kleymo = self._get_value(row_tree, "//tr[@bgcolor]/td[2]/span/text()")
            company = self._get_value(row_tree, "//tr[@bgcolor]/td[3]/text()")
            job_title = self._get_value(row_tree, "//tr[@bgcolor]/td[4]/text()")
            certification_number = self._get_value(row_tree, "//tr[@bgcolor]/td[5]/text()")
            insert = self._get_value(row_tree, "//tr[@bgcolor]/td[6]/text()")
            certification_date = self._get_value(row_tree, "//tr[@bgcolor]/td[9]/text()", True)
            expiration_date = self._get_value(row_tree, "//tr[@bgcolor]/td[10]/text()", True)
            renewal_date = self._get_value(row_tree, "//tr[@bgcolor]/td[11]/text()", True)

            result.append({
                "full_name": name,
                "kleymo": kleymo,
                "company": company,
                "job_title": job_title,
                "certification_number": certification_number,
                "insert": insert,
                "certification_date": certification_date,
                "expiration_date": expiration_date,
                "renewal_date": renewal_date,
                "certification_id": self._get_certification_id(kleymo, certification_number, certification_date, insert)
                }
            )

        return result
    

    def _extract_data_from_welder_certification_page(self, welder_certification_page: str) -> dict[str, str]:
        result = {}
        tree = html.fromstring(welder_certification_page)

        trs: list[html.HtmlElement] = tree.xpath("//tr")

        for tr in trs:
            tds: list[html.HtmlElement] = tr.getchildren()

            if len(tds) < 2:
                continue

            key = tds[0].text

            value = " | ".join([td.text_content() for td in tds[1:]])

            if key == "Положение при сварке":
                value = value.replace("\r\n", " ")

            result[key] = value

        return result


    def _get_certification_id(self, kleymo: str, certification_number: str, certification_date: date, insert: str | None) -> str:
        if insert == None:
            insert = ""
        
        chars = findall(r"[\w]", str(kleymo) + str(certification_number) + str(certification_date) + str(insert))
        
        return "".join(chars).lower()
    

    def _get_value(self, tree: html.HtmlElement, xpath: str, is_date: bool = False) -> str | date | None:
        try:
            if is_date:
                return str_to_date(tree.xpath(xpath)[0])
            
            return tree.xpath(xpath)[0].strip()
        except:
            return None



class EngineerDataExtractor(IExtractor): ...