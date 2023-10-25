from typing import (
    Literal,
    TypeVar,
    TypeAlias,
    Union,
    Any
)
from datetime import date, datetime
from pathlib import Path
import os

from openpyxl.styles import Alignment, PatternFill, Border, Side
from openpyxl.worksheet.worksheet import Worksheet
from openpyxl.chart import LineChart, Reference
from openpyxl import load_workbook, Workbook
from openpyxl.cell.cell import Cell


AnyType: TypeAlias = Union[str, int, float, date, datetime]


class ExcelService:
    @staticmethod
    def load_file(path: str | Path, **kwargs) -> Workbook:
        if not os.path.exists(path):
            raise FileNotFoundError(path)

        return load_workbook(path, **kwargs)


    @staticmethod
    def create_file(**kwargs) -> Workbook:
        wb = Workbook(**kwargs)

        return wb
    

    def data_to_cells(self, data: list[Any], ws: Worksheet) -> list[Cell]:
        return [
            Cell(worksheet=ws, value=el) for el in data
        ]
    

    def read_worksheet_by_row(self, ws: Worksheet, **kwargs) -> list[list[AnyType]]:
        return [
            list(row) for row in ws.iter_rows(**kwargs)
        ]
    

    def read_worksheet_by_column(self, ws: Worksheet, **kwargs) -> list[list[AnyType]]:
        return [
            list(column) for column in ws.iter_cols(**kwargs)
        ]


    def style_rows(self, rows: list[list[Cell]], mode: Literal["header", "body"]) -> list[Cell]:
        match mode:
            case "header":
                return self._style_like_header_rows(rows)
            
            case "body":
                return self._style_like_body_rows(rows)
            
            case _:
                raise ValueError("Invalid mode")


    def get_line_chart(self, ws: Workbook, reference: Reference, **kwargs) -> LineChart:
        
        chart = LineChart()

        chart.title = kwargs.get("chart_title", "default chart name")

        chart.x_axis.crossAx = kwargs.get("x_crossAx", 100)
        chart.y_axis.crossAx = kwargs.get("y_crossAx", 500)

        chart.x_axis.title = kwargs.get("x_axis_title", "default name")

        chart.y_axis.title = kwargs.get("y_axis_title", "default name")

        chart.width = kwargs.get("chart_width", 15)
            
        chart.height = kwargs.get("chart_height", 7.5)
        
        data = Reference(ws, **kwargs)

        chart.add_data(data, titles_from_data=True)
        chart.set_categories(reference)
        
        match kwargs.get("style"):
            case "default":
                chart.style = 12
            case _:
                chart.style = 12

        return chart
    

    def add_chart(self, ws: Worksheet, chart, coordinate: str) -> None:
        ws.add_chart(chart, coordinate)

    
    def _style_like_header_rows(self, rows: list[list[Cell]]) -> list[Cell]:
        styled_rows = []

        for row in rows:
            styled_row = []

            for cell in row:
                styled_row.append(
                    self._set_header_cell_style(cell)
                )
            
            styled_rows.append(styled_row)
        
        return styled_rows


    def _style_like_body_rows(self, rows: list[list[Cell]]) -> list[Cell]:
        styled_rows = []

        for e, row in enumerate(rows):
            styled_row = []

            for cell in row:
                styled_row.append(
                    self._set_body_cell_style(cell, e)
                )
            
            styled_rows.append(styled_row)
        
        return styled_rows

    
    def _set_header_cell_style(self, cell: Cell) -> Cell:
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.fill = PatternFill(start_color='003366FF', end_color='003366FF', fill_type='solid')
        cell.border = Border(
            right = Side(color="FF000000", style="thin")
        )

        return cell


    def _set_body_cell_style(self, cell: Cell, e: int) -> Cell:
        cell.alignment = Alignment(horizontal='center', vertical='center')
        cell.border = Border(
            right = Side(color="FF000000", style="thin")
        )

        if e % 2 == 1:
            cell.fill = PatternFill(start_color='00CCFFFF', end_color='00CCFFFF', fill_type='solid')

        if e % 2 == 0:
            cell.fill = PatternFill(start_color='0033CCCC', end_color='0033CCCC', fill_type='solid')

        return cell
