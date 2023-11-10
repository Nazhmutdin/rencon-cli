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



    def execute(self, mode: Literal["a", "u", "r"]) -> None:
        mode = mode.lower()
        welders = self._get_welders()

        match mode:
            case "a":
                self.repo.add(welders)

            case "u":
                self.repo.update(welders)

            case "r":
                self.repo.delete(welders)
            
            case _:
                echo("Invalid mode")
