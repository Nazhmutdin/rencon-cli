from typing import Any

from src.domain import WelderNDTModel
from src.services import ExcelService


class NDTReportParser:
    excel = ExcelService()


    def parse(self, path: str) -> list[WelderNDTModel]:
        file_data = self._extract_file_data(path)

        return self._convert_to_model(file_data)


    def _convert_to_model(self, data: list[list[Any]]) -> list[WelderNDTModel]:
        result: list[WelderNDTModel] = []
        model_fields = list(WelderNDTModel.model_fields.keys())

        for row_data in data:
            row_data[3] = None if row_data[3] == "" else row_data[3]
            ndt = WelderNDTModel(**{model_fields[i]: row_data[i] for i in range(len(model_fields) - 1)})
            ndt.set_id()

            result.append(ndt)
        

        return result

    
    def _extract_file_data(self, path: str) -> list[list[Any]]:
        wb = self.excel.load_file(path)

        ws = wb.active

        return [
            row_data[2:27] for row_data in self.excel.read_worksheet_by_row(ws, values_only=True, min_row=4)
        ]
