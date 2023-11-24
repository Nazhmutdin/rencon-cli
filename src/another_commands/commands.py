from typing import Literal
from re import fullmatch
import os

from click import Command, Option, echo

from src.db.repository import WelderRepository
from src.domain import WelderRequest
from settings import GROUPS_FOLDER


class RenameFolderCommand(Command):

    def __init__(self) -> None:
        name = "rename-folders"

        mode_option = Option(["--mode", "-m"], type=str, help="w - rename welder folder\n\ne - rename engineer folder")
        folder_option = Option(["--folder", "-f"], type=str, help="group folder")

        super().__init__(name=name, params=[mode_option, folder_option], callback=self.execute)

    
    def execute(self, mode: Literal["w", "e"], folder: str) -> None:
        mode = mode.lower()
        match mode:
            case "w":
                self._rename_welder_folder(folder)

            case "e":
                echo("Not implemented yet")

            case _:
                print("unknown mode")

    
    def _rename_welder_folder(self, folder: str) -> None:
        repo = WelderRepository()

        welder_folders = [welder_folder for welder_folder in os.listdir(f"{GROUPS_FOLDER}/{folder}") if not fullmatch(r"[A-Z0-9]{4}", welder_folder.split("_")[0])]

        welders = repo.get_many(
            WelderRequest(
                names=welder_folders
            )
        )

        welder_dict: dict[str, list[str]] = {}

        for welder in welders:
            if welder.full_name not in welder_dict:
                welder_dict[welder.full_name] = [welder.kleymo]
                continue

            welder_dict[welder.full_name].append(welder.kleymo)

        for name, kleymos in welder_dict.items():
            os.rename(f"{GROUPS_FOLDER}/{folder}/{name}", f"{GROUPS_FOLDER}/{folder}/{"_".join(kleymos)}_{name}")
