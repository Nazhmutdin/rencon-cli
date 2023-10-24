from click import Command, Option
from os import listdir
from typing import (
    Sequence,
    TypeAlias
)

from .parsers import PersonalParser
from .extractors import WelderDataExtractor, IExtractor
from src.domain import WelderModel
from src.services.utils import load_json
from settings import SEARCH_VALUES_FILE, GROUPS_FOLDER


Name: TypeAlias = str
Kleymo: TypeAlias = str


class ParsePersonalCommand(Command):
    def __init__(self) -> None:
        name = "parse-personal"

        mode_option = Option(["--mode", "-m"], type=str)
        file_option = Option(["--file"], type=bool)
        folder_option = Option(["--folder"], type=str)

        super().__init__(name=name, params=[mode_option, file_option, folder_option], callback=self.execute)
    
    
    def _read_search_values_file(self) -> Sequence[Name | Kleymo]:
        settings = load_json(SEARCH_VALUES_FILE)["personal_naks_parsing"]

        return settings["search_values"]


    def execute(self, mode: str, file: str | None = None, folder: str | None = None) -> None:
        parser = PersonalParser()
        values = []

        if file:
            values += self._read_search_values_file()

        if folder:
            values += [value for value in listdir(f"{GROUPS_FOLDER}/{folder}")]
        

    
    def _set_extractor(self, mode: str) -> IExtractor[WelderModel]: ...