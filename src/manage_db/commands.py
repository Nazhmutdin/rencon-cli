from typing import Literal
from json import load

from click import Command, Option, echo

from src.db.repository import WelderCertificationRepository, WelderRepository
from src.manage_db.help_messages import welder_table_mode_option_help_message
from src.domain import WelderCertificationModel, WelderModel
from settings import WELDERS_DATA_JSON_PATH


class ManageWelderDataCommand(Command):
    def __init__(self) -> None:
        name = "manage-welder-data"
        self.repo = WelderRepository()

        mode_option = Option(["--mode", "-m"], type=str, help=welder_table_mode_option_help_message)

        super().__init__(name=name, params=[mode_option], callback=self.execute)

    
    def _get_welders(self) -> list[WelderModel]:
        return load(open(WELDERS_DATA_JSON_PATH, "r", encoding="utf-8"))


    def _add(self, welders: list[WelderModel]) -> None:
        self.repo.add(welders)


    def _update(self, welders: list[WelderModel]) -> None:
        self.repo.update(welders)


    def _remove(self, welders: list[WelderModel]) -> None: ...


    def execute(self, mode: Literal["a", "u", "r"]) -> None:
        mode = mode.lower()
        welders = self._get_welders()

        match mode:
            case "a":
                self._add(welders)

            case "u":
                self._update(welders)

            case "r":
                self._remove(welders)
            
            case _:
                echo("Invalid mode")
