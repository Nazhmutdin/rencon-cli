from os import listdir
from time import sleep
from typing import (
    Sequence,
    TypeAlias
)
import json

from click import Command, Option

from src.parse_naks.extractors import IExtractor, WelderDataExtractor, EngineerDataExtractor
from settings import SEARCH_VALUES_FILE, GROUPS_FOLDER, WELDERS_DATA_JSON_PATH
from src.services.utils import ThreadProgressBarQueue
from src.parse_naks.workers import PersonalNaksWorker
from src.services.utils import load_json
from src.parse_naks.sorter import Sorter
from src.parse_naks.types import Model


Name: TypeAlias = str
Kleymo: TypeAlias = str


class ParsePersonalCommand(Command):
    def __init__(self) -> None:
        name = "parse-personal"

        mode_option = Option(["--mode", "-m"], type=str, default="-", help="modes: w - welder, e - engineer")
        file_option = Option(["--file"], type=bool, help="get search values from search_settings.json file")
        folder_option = Option(["--folder"], type=str, help="get folder's names in folder as search_values")
        threads_option = Option(["--threads", "-t"], type=int, default=1, help="amount threads")

        super().__init__(name=name, params=[mode_option, file_option, folder_option, threads_option], callback=self.execute)
    
    
    def _read_search_values_file(self) -> Sequence[Name | Kleymo]:
        settings = load_json(SEARCH_VALUES_FILE)["personal_naks_parsing"]

        return settings["search_values"]


    def _set_extractor(self, mode: str) -> IExtractor: 

        match mode:
            case "w":
                return WelderDataExtractor()
            case "e":
                return EngineerDataExtractor()
            

    def _fill_queue(self, queue: ThreadProgressBarQueue, file: str | None, folder: str | None) -> None:

        if file:
            for value in self._read_search_values_file():
                queue.put(value)

        if folder:
            for value in [value for value in listdir(f"{GROUPS_FOLDER}/{folder}")]:
                queue.put(value)

        
    def _init_threads(self, threads: int, queue: ThreadProgressBarQueue, stack: list[Model], extractor: IExtractor) -> None:
        ths: list[PersonalNaksWorker] = []

        for _ in range(threads):
            thread = PersonalNaksWorker(queue, stack, extractor)

            thread.start()
            ths.append(thread)

        for th in ths:
            th.join()
        sleep(.1)


    def execute(self, mode: str, threads: int, file: str | None = None, folder: str | None = None) -> None:
        queue = ThreadProgressBarQueue()
        self._fill_queue(queue, file, folder)

        stack: list[Model] = []

        mode = mode.lower()

        if mode not in ["w", "e"]:
            print("Invalid mode")
            return

        extractor = self._set_extractor(mode)
        queue.init_progress_bar()
        self._init_threads(threads, queue, stack, extractor)

        sorter = Sorter()

        stack = [el.model_dump(mode="json") for el in sorter.sort_welder_data(stack)]

        with open(WELDERS_DATA_JSON_PATH, "w", encoding="utf-8") as file:
            json.dump(stack, file, indent=4, ensure_ascii=False)
            file.close()
