from dataclasses import dataclass
from datetime import datetime, date
from typing import (
    Sequence, 
    Literal,
    TypeAlias
)
from re import fullmatch

from requests import Session, Response
from lxml import html

from src.domain import WelderModel, WelderCertificationModel


"""
=======================================================================================================
Types
=======================================================================================================
"""


Name: TypeAlias = str
Kleymo: TypeAlias = str
Link: TypeAlias = str


"""
=======================================================================================================
Domain Layer
=======================================================================================================
"""


@dataclass
class WelderPageRowData:
    full_name: str | None = None
    kleymo: str | None = None
    job_title: str | None = None
    company: str | None
    certification_date: date
    expiration_date: date
    renewal_date: date | None = None
    certification_number: str


@dataclass
class WelderCertificationPageData:
    certification_number: str
    certification_type: str | None
    method: str | None
    details_type: str | None
    joint_type: str | None
    groups_materials_for_welding: str | None
    welding_materials: str | None
    details_thikness: str | None
    outer_diameter: str | None
    welding_position: str | None
    connection_type: str | None
    rod_diameter: str | None
    rod_axis_position: str | None
    weld_type: str | None
    joint_layer: str | None
    gtd: str | None
    sdr: str | None
    automation_level: str | None
    details_diameter: str | None
    welding_equipment: str | None

@dataclass
class WelderData:
    full_name: str | None = None
    kleymo: str | None = None
    job_title: str | None = None
    company: str | None
    certification_date: date
    expiration_date: date
    renewal_date: date | None = None
    certification_number: str
    certification_type: str | None
    method: str | None
    details_type: str | None
    joint_type: str | None
    groups_materials_for_welding: str | None
    welding_materials: str | None
    details_thikness: str | None
    outer_diameter: str | None
    welding_position: str | None
    connection_type: str | None
    rod_diameter: str | None
    rod_axis_position: str | None
    weld_type: str | None
    joint_layer: str | None
    gtd: str | None
    sdr: str | None
    automation_level: str | None
    details_diameter: str | None
    welding_equipment: str | None


class WelderDataExtractor:
    welder_page: str
    certification_Pages: Sequence[str]


    def _extract_data_from_welder_page(self, welder_page: str) -> tuple(Sequence[WelderPageRowData], Sequence[Link]):
        ...

    
    def _extract_data_from_welde_certification_page(self, welder_certification_page: str) -> WelderPageRowData:
        ...


    def extract(self) -> WelderModel: ...


"""
=======================================================================================================
Infrastructure Layer
=======================================================================================================
"""


class NaksPersonalSession(Session):
    def __init__(self) -> None:
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Origin': 'https://naks.ru',
            'Referer': 'https://naks.ru/registry/personal/',
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
        }

        self.url = 'https://naks.ru/registry/personal/'

        self.data = 'arrFilter_pf%5Bap%5D=&arrFilter_ff%5BNAME%5D={name}&arrFilter_pf%5Bshifr_ac%5D=&arrFilter_pf%5Buroven_ac%5D=&arrFilter_pf%5Bnum_ac%5D=&arrFilter_ff%5BCODE%5D={kleymo}&arrFilter_DATE_CREATE_1=&arrFilter_DATE_CREATE_2=&arrFilter_DATE_ACTIVE_TO_1=&arrFilter_DATE_ACTIVE_TO_2=&arrFilter_DATE_ACTIVE_FROM_1=&arrFilter_DATE_ACTIVE_FROM_2=&g-recaptcha-response=&set_filter=%D4%E8%EB%FC%F2%F0&set_filter=Y'


    def post(self, search_value: Kleymo | Name) -> Response:
        self._set_request_data(search_value)

        return super().post(self.url, data=self.data)
    
    
    def _set_request_data(self, search_value: Kleymo | Name) -> None:
        value_type = self._detect_search_value_type(search_value)

        if value_type == "kleymo":
            self.data.format(kleymo=search_value)

        else:
            self.data.format(name=search_value)
    

    def _detect_search_value_type(self, search_value: str) -> Literal["name", "kleymo"]:
        if fullmatch(r"[A-Z0-9]{4}", search_value.strip()):
            return "kleymo"
        
        return "name"




class SaveJsonService:
    def save(self) -> None: ...