from typing import (
    Sequence,
    TypeAlias
)

from src.services.utils import load_json
from .services import NaksPersonalSession
from settings import SEARCH_VALUES_FILE


"""
=======================================================================================================
Types
=======================================================================================================
"""


Name: TypeAlias = str
Kleymo: TypeAlias = str


"""
=======================================================================================================
Parser
=======================================================================================================
"""


class PersonalParser:
    session = NaksPersonalSession()


    def _get_search_values(self) -> Sequence[Name | Kleymo]:
        settings = load_json(SEARCH_VALUES_FILE)["personal_naks_parsing"]

        return settings["search_values"]


    def parse(self) -> None:
        values = self._get_search_values()

        