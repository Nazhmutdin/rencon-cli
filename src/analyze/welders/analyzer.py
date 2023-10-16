from typing import Literal

from .services import ExcelResultSaveService, PDFResultSaveService, Saver
from src.domain import DBResponse


class WelderAnalyzer:
    savers = {
        "excel": ExcelResultSaveService,
        "pdf": PDFResultSaveService,
    }

    def _set_saver(self, mode: Literal["excel", "pdf"]) -> None:
        self.saver: Saver = self.savers[mode]()


    def analyze_ndts(self, mode: Literal["excel", "pdf"], row_data: DBResponse) -> None:
        self._set_saver(mode)
