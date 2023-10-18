import json
from typing import Union

from src.db.repository import WelderCertificationRepository, WelderRepository, Repository
from src.domain import WelderCertificationModel, WelderModel, DomainModel
from settings import WELDERS_DATA_JSON_PATH


class WelderAppendModeExecutionService:
    data_json = json.load(open(WELDERS_DATA_JSON_PATH, "r", encoding="utf-8"))

    def _data_to_domain_models(self) -> None:
        return [
            WelderModel.model_validate()
        ]


class WelderUpdateModeExecutionService:
    ...