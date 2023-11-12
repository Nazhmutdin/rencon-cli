from typing import Literal
from json import load

from click import Command, Option, echo

from src.db.repository import WelderRepository
from src.domain import WelderModel
from settings import WELDERS_DATA_JSON_PATH


class ManageWelderDataCommand(Command):
    def __init__(self) -> None:
        name = "manage-welder-data"
        self.repo = WelderRepository()

        mode_option = Option(["--mode", "-m"], type=str, help="a-add\n\nu-update\n\nd-delete")

        super().__init__(name=name, params=[mode_option], callback=self.execute)


    @property
    def _welders(self) -> list[WelderModel]:
        return [WelderModel.model_validate(welder_dict) for welder_dict in load(open(WELDERS_DATA_JSON_PATH, "r", encoding="utf-8"))]


    def execute(self, mode: Literal["a", "u", "d"]) -> None:
        mode = mode.lower()

        match mode:
            case "a":
                self.repo.add(self._welders)

            case "u":
                self.repo.update(self._welders)

            case "d":
                self.repo.delete(self._welders)
            
            case _:
                echo("Invalid mode")
