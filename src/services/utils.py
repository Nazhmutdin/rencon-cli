from typing import Mapping

from pathlib import Path
from json import load


def load_json(path: str | Path) -> Mapping:
    return load(open(path, "r", encoding="utf-8"))