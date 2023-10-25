from typing import (
    TypeAlias,
    TypeVar,
    Sequence,
)
from pathlib import Path
from datetime import date
import os

from openpyxl.worksheet.worksheet import Worksheet
from openpyxl import Workbook
from numpy import ndarray
from pdf2image import convert_from_path
import cv2 as cv

from settings import ACT_DATA_FILES_PATH, PATH_TO_POPPLER
from src.services import ExcelService, OpenCVSevice


"""
=======================================================================================================
Types
=======================================================================================================
"""





"""
=======================================================================================================
Domain Services
=======================================================================================================
"""


class ActRegistryService:

    def update_registry(self, folder: str) -> None:
        # images = ReadInvoiceFileService().read(folder)
        self._extract_excel_data(folder)
        self._extract_invoices_data(folder)

        
    def _extract_excel_data(self, folder: str) -> dict[str, tuple[str, str, str]]:
        service = ExcelService()
        wb = ReadReportFileService().read(folder)

        rows = service.read_worksheet_by_row(
            wb.active,
            min_row=3,
            max_col=13,
            min_col=3,
            values_only=True
        )

        return self._parse_rows(rows)


    def _extract_invoices_data(self, folder: str) -> dict[str, tuple[str, str, str]]:
        images = ReadInvoiceFileService().read(folder)
        service = OpenCVSevice()

        service._to_absolute_coordinates(list(images.values())[0][0], [1, 3, 5, 7])


    def _parse_rows(self, rows: list[str]) -> dict[str, tuple[str, str, str]]:
        result = {}

        for row in rows :
            row_result = (
                *self._extract_project_sumcomp(row[0]),
                row[-2].strip().title(),
            )

            result[row[-1].strip().title()] = row_result
        
        return result
    
    
    def _extract_project_sumcomp(self, project_sumcomp_string: str) -> tuple[str, str]:
        parts = project_sumcomp_string.split("(")
        return (
            parts[0].strip(),
            parts[1].replace(")", "").strip()
        )


"""
=======================================================================================================
Infrastructure Services
=======================================================================================================
"""


class ReadReportFileService:

    def _get_excel_report_path(self, folder: str | Path) -> str | Path:
        files = os.listdir(f"{ACT_DATA_FILES_PATH}/{folder}")

        for file in files:
            if file.endswith(".xlsx"):
                return f"{ACT_DATA_FILES_PATH}\{folder}\{file}"
    
    
    def read(self, folder: str) -> Workbook:
        path = self._get_excel_report_path(folder)
        return ExcelService.load_file(path)


class ReadInvoiceFileService:

    def _get_invoices_path(self, folder: str | Path) -> list[str | Path]:
        files = os.listdir(f"{ACT_DATA_FILES_PATH}/{folder}")

        return [
            f"{ACT_DATA_FILES_PATH}\{folder}\{file}" for file in files if file.endswith(".pdf")
        ]
    
    def read(self, folder: str) -> dict[str, ndarray]:
        files = self._get_invoices_path(folder)
        images = {}

        for file in files:
            images[file.split("\\")[-1]] = [
                OpenCVSevice.image_to_array(image) for image in convert_from_path(file, poppler_path=PATH_TO_POPPLER)
            ]
    
        return images
