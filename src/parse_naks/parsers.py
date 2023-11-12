from time import sleep
from typing import (
    TypeAlias
)

from re import fullmatch
from requests import Session

from src.parse_naks.extractors import WelderDataExtractor


"""
=======================================================================================================
Types
=======================================================================================================
"""


Name: TypeAlias = str
Kleymo: TypeAlias = str
MainPage: TypeAlias = str
AdditionalPage: TypeAlias = str


"""
=======================================================================================================
Parser
=======================================================================================================
"""


class PersonalParser:

    def __init__(self) -> None:
        self.session = Session()
        self.session.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Referer': 'https://naks.ru/registry/personal/',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36'
        }

        self.url = 'https://naks.ru/registry/personal/'

        self.data = 'arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac%5D=&arrFilter_pf%5Buroven_ac%5D=&arrFilter_pf%5Bnum_ac%5D=&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'
    

    def _set_request_data(self, search_value: str) -> Kleymo | Name:
        data = self.data

        if fullmatch(r"[A-Z0-9]{4}", search_value.strip()):
            data = data.format(kleymo=search_value.strip(), name="")
            return data
        
        name = repr(search_value.encode("windows-1251"))[2:-1].replace("\\x", "%").upper().replace(" ", "+")
        data = data.format(name=name, kleymo="")
        return data


    def parse(self, value: str) -> tuple[MainPage, list[AdditionalPage]]:

        data = self._set_request_data(value)
        res = self.session.post(self.url, data)
        sleep(1)
        main_page = res.text
        additional_pages = []

        links = WelderDataExtractor.extract_links(res.text)

        for link in links:
            additional_pages.append(self.session.get(link).text)
            sleep(.5)
        
        return (main_page, additional_pages)
