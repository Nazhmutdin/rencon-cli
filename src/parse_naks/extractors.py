from abc import ABC, abstractmethod
from dataclasses import dataclass
from re import search
from datetime import date
from typing import (
    Generic,
    Sequence, 
    TypeAlias,
    TypeVar
)

from lxml import html
from pydantic import BaseModel

from src.domain import WelderModel, WelderCertificationModel


"""
=======================================================================================================
Types and Value-objects
=======================================================================================================
"""


Name: TypeAlias = str
Kleymo: TypeAlias = str
Link: TypeAlias = str
Model = TypeVar("Model", bound=BaseModel)


@dataclass
class Pages:
    welder_page: str
    certifications_page: str

   
@dataclass
class WelderData:
    full_name: str | None = None
    kleymo: str | None = None
    job_title: str | None = None
    company: str | None = None
    certification_date: date = None
    expiration_date: date = None
    renewal_date: date | None = None
    certification_number: str = None
    certification_type: str | None = None
    method: str | None = None
    details_type: str | None = None
    joint_type: str | None = None
    groups_materials_for_welding: str | None = None
    welding_materials: str | None = None
    details_thikness: str | None = None
    outer_diameter: str | None = None
    welding_position: str | None = None
    connection_type: str | None = None
    rod_diameter: str | None = None
    rod_axis_position: str | None = None
    weld_type: str | None = None
    joint_layer: str | None = None
    gtd: str | None = None
    sdr: str | None = None
    automation_level: str | None = None
    details_diameter: str | None = None
    welding_equipment: str | None = None


"""
=======================================================================================================
Extractors
=======================================================================================================
"""


class IExtractor(ABC, Generic[Model]):

    @abstractmethod
    def extract(self, main_page: str, additional_pages: Sequence[str]) -> Model: ...


class WelderDataExtractor(IExtractor):

    def _extract_data_from_welder_page(self, welder_page: str) -> Sequence[Sequence[str]]:
        result = {}
        tree = html.fromstring(welder_page)

        names = tree.xpath("//tr[@bgcolor]/td[1]/text()")
        kleymos = tree.xpath("//tr[@bgcolor]/td[2]/span/text()")
        companies = tree.xpath("//tr[@bgcolor]/td[3]/text()")
        job_titles = tree.xpath("//tr[@bgcolor]/td[4]/text()")
        certification_numbers = tree.xpath("//tr[@bgcolor]/td[5]/text()")
        inserts = tree.xpath("//tr[@bgcolor]/td[6]/text()")
        certification_dates = tree.xpath("//tr[@bgcolor]/td[9]/text()")
        expiration_dates = tree.xpath("//tr[@bgcolor]/td[10]/text()")
        renewal_dates = tree.xpath("//tr[@bgcolor]/td[11]/text()")

        return 

    
    def _extract_data_from_welder_certification_page(self, welder_certification_page: str) -> dict[str, str]:
        ...

    
    @staticmethod
    def extract_links(welder_page: str) -> Sequence[Link]:
        tree = html.fromstring(welder_page)
        links = tree.xpath("//tr[@bgcolor]/td[13]/a/@onclick")
        links = [search(r"/[\w]+/[\w]+/detail.php\?ID=[\w\W]+", link)[0].replace('"', '').split(",")[0] for link in links]

        links = [f"https://naks.ru{link}" for link in links]

        return links
    

    def extract(self, main_page: str, additional_pages: Sequence[str]) -> WelderModel: ...
