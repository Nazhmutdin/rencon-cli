from typing import (
    Any
)
from pathlib import Path
import re
import os


from settings import ACT_DATA_FILES_PATH
from src.services import ExcelService
from src.manage_registry.types import InvoiceRow, WelderListRow
from src.services.utils import str_to_date


class ActRegistryService:

    def update_registry(self, folder: str) -> None:
        invoices, welders = self._get_invoices_welders(folder)
        date = str_to_date(folder)

        for invoice in invoices:
            invoice.names = self._get_names(invoice.service_name)
            invoice.methods = self._get_methods(invoice.service_name)
        
        print(invoices)


    def _get_invoices_welders(self, folder: str) -> tuple[list[InvoiceRow], list[WelderListRow]]:
        path = f"{ACT_DATA_FILES_PATH}/{folder}"
        files = [file for file in os.listdir(path) if file.endswith(".xlsx") and file != "welder_list.xlsx"]
        service = ReadExcelFileService()
        invoices = service.read_invoice_file(f"{path}/{files[0]}")
        welders = service.read_welder_list_file(f"{path}/welder_list.xlsx")

        return (invoices, welders)


    def _get_names(self, string: str) -> list[str] | None:
        strings = string.split(")")[1].split(",")

        if strings == [""]:
            return
        
        name = re.compile(r"[А-Яа-я ]+")

        return [name.search(string)[0].strip() for string in strings]
    

    def _get_methods(self, string: str) -> list[str] | None:
        string = re.search(r"\([\W\w]+\)", string)[0]

        return re.findall(r"[А-Я]{2,}", string)


class ReadExcelFileService:
    def _read_excel(self, path: str | Path) -> list[list[Any]]:
        service = ExcelService()
        wb = service.load_file(path)
        data = service.read_worksheet_by_row(wb.active, values_only=True, min_row=2, min_col=2)
        return data


    def read_invoice_file(self, path: str | Path) -> list[InvoiceRow]:
        data = self._read_excel(path)

        return [
            InvoiceRow(
                service_name=row[0].strip().replace("\n", " "),
                amount=row[1],
                price=row[3]
            ) for row in data
        ]


    def read_welder_list_file(self, path: str | Path) -> list[WelderListRow]:
        data =self._read_excel(path)

        return [
            WelderListRow(
                full_name=row[0].strip().replace("\n", " "),
                full_name_rus=row[1].strip().replace("\n", " "),
                project=row[2].strip().replace("\n", " "),
                subcomp=row[3].strip().replace("\n", " "),
                method=row[4].strip().replace("\n", " "),
            ) for row in data
        ]
