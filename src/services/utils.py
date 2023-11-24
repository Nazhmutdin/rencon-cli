from typing import Mapping, Sequence, TypeVar, Any
from dateutil.parser import parser
from queue import Queue
from re import compile

from pathlib import Path
from rich.progress import Progress, BarColumn, TaskProgressColumn, MofNCompleteColumn, TimeElapsedColumn, TimeRemainingColumn
from json import load

DictKey = TypeVar("DictKey")
DictValue = TypeVar("DictValue")
DictSequenceValue = TypeVar("DictSequenceValue")
numbers = compile(r"[0-9]+")


class ThreadProgressBarQueue(Queue):

    def init_progress_bar(self) -> None:
        progress_columns = (
            "[blue]Processing...", 
            BarColumn(), 
            TaskProgressColumn(),
            "[blue]processed: ",
            MofNCompleteColumn(),
            TimeElapsedColumn(),
            "[blue]remaining: ",
            TimeRemainingColumn()
        )
        self.progress_bar = Progress(*progress_columns)
        self.progress_bar.start()
        self.task = self.progress_bar.add_task("Processing", total=self.qsize(), )


    def get(self, block: bool = True, timeout: float | None = None) -> Any:
        self.progress_bar.update(self.task, advance=1)
        return super().get(block, timeout)


def load_json(path: str | Path) -> Mapping:
    return load(open(path, "r", encoding="utf-8"))


def str_to_date(date_string: str):
    try:
        return parser().parse(date_string).date()

    except:
        raise ValueError("Invalid date")


def reverse_dict(rows_dict: dict[DictKey, DictValue]) -> dict[DictKey, DictValue]:
    return dict(
        reversed(
            list(
                rows_dict.items()
            )
        )
    )


def limit_dict_pair(data_dict: dict[DictKey, Sequence[DictSequenceValue]], limit: int | None) -> dict[DictKey, list[DictSequenceValue]]:
    
    return {
        key: value for e, (key, value) in enumerate(data_dict.items()) if e < limit
    }


def limit_dict_values(data_dict: dict[DictKey, DictSequenceValue], limit: int) -> dict[DictKey, DictSequenceValue]:
    limited_dict: dict[DictKey, DictSequenceValue] = {}

    for key, values in data_dict.items():
        if key not in limited_dict:
            limited_dict[key] = []

        for value in values:

            if len(limited_dict[key]) < limit:
                limited_dict[key].append(value)
    
    return limited_dict
