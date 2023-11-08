import json
from typing import Union

from src.db.repository import WelderCertificationRepository, WelderRepository
from src.domain import WelderCertificationModel, WelderModel
from settings import WELDERS_DATA_JSON_PATH


class WelderDBService:
    repo = WelderRepository()

    def add(self, welders: list[WelderModel]) -> None:
        self.repo.add(welders)


    def update(self, welders: list[WelderModel]) -> None: ...


    def delete(self, welders: list[WelderModel]) -> None: ...
