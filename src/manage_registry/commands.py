from pathlib import Path
import json
import os
import typing as t

from click import Command, Option

from settings import NDT_TABLES_FOLDER_PATH, SEARCH_VALUES_FILE, WELDERS_DATA_JSON_PATH
from .parse_ndt_report_service import NDTReportParser
from .manage_welder_registry_service import WelderRegistryManager
from src.db.repository import NDTRepository, WelderRepository
from src.domain import WelderNDTModel, WelderModel


class ManageActsRegistryCommand(Command):
    def __init__(self) -> None:

        name = 'manage-act-registry'

        folder_option = Option(['--folder', '-f'], type=str, help='w')

        super().__init__(name=name, params=[folder_option], callback=self.execute)


    def execute(self, folder: str | Path) -> None:
        print("Not implemented")


class ManageWelderRegistryCommand(Command):
    
    def __init__(self) -> None:
        name = "manage-welder-registry"

        group_key_option = Option(["--group_key"], type=str)
        subgroup_option = Option(["--subgroup"], type=str)
        group_option = Option(["--group"], type=str)

        super().__init__(name=name, params=[group_key_option, subgroup_option, group_option], callback=self.execute)


    def execute(self, group: str, group_key: str, subgroup: str) -> None:
        manager = WelderRegistryManager()

        manager.update(
            self._read_welder_json_file(),
            group_key,
            subgroup,
            group
        )


    def _read_welder_json_file(self) -> list[WelderModel]:
        with open(WELDERS_DATA_JSON_PATH, "r", encoding="utf-8") as file:
            data = json.load(file)
            file.close()

        return [
            WelderModel.model_validate(el) for el in data
        ]


class ParseNDTReport(Command):
    def __init__(self) -> None:
        name = "parse-ndt-report"

        folder_option = Option(["--folder"], type=str)

        super().__init__(name=name, params=[folder_option], callback=self.execute)


    def execute(self, folder: str) -> None:
        path = f"{NDT_TABLES_FOLDER_PATH}/{folder}"
        if not os.path.exists(path):
            raise FileNotFoundError(f"folder {folder} doesn't exists")
        
        parser = NDTReportParser()
        repo = NDTRepository()

        files = [file for file in os.listdir(path) if file.endswith(".xlsx")]
        ndts = []

        for file in files:
            ndts += parser.parse(f"{path}/{file}")

        if not self._check_welders_in_db(ndts):
            print("Not all welders in db")
            self._add_kleymo_to_search_settings(ndts)
            return 
        
        repo.add(ndts)

        
    def _check_welders_in_db(self, ndts: list[WelderNDTModel]) -> bool:
        repo = WelderRepository()
        for el in ndts:
            if not repo.get(el.kleymo):
                return False

        return True
    

    def _add_kleymo_to_search_settings(self, ndts: list[WelderNDTModel]) -> None:
        search_settings = json.load(open(SEARCH_VALUES_FILE, "r", encoding="utf-8"))

        kleymos = [ndt.kleymo for ndt in ndts]

        search_settings["personal_naks_parsing"]["search_values"] = kleymos

        with open(SEARCH_VALUES_FILE, "w", encoding="utf-8") as file:
            json.dump(search_settings, file, indent=4, ensure_ascii=False)
            file.close()
