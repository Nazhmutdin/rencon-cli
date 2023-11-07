from dataclasses import dataclass
from datetime import date
from typing import (
    TypeAlias,
    TypeVar
)

from pydantic import BaseModel, ConfigDict, Field


Name: TypeAlias = str
Kleymo: TypeAlias = str
Link: TypeAlias = str
Model = TypeVar("Model", bound=BaseModel)


@dataclass
class Pages:
    welder_page: str
    certifications_page: str


class WelderData(BaseModel):
    full_name: str | None = Field(default=None)
    kleymo: str | None = Field(default=None)
    job_title: str | None = Field(default=None)
    company: str | None = Field(default=None, alias="Место работы (организация, инн):")
    certification_date: date | None = Field(default=None)
    expiration_date: date | None = Field(default=None)
    renewal_date: date | None = Field(default=None)
    certification_number: str | None = Field(default=None)
    certification_type: str | None = Field(default=None, alias="Вид аттестации:")
    insert: str | None = Field(default=None)
    method: str | None = Field(default=None, alias="Вид (способ) сварки (наплавки)")
    details_type: str | None = Field(default=None, alias="Вид деталей")
    joint_type: str | None = Field(default=None, alias="Типы швов")
    groups_materials_for_welding: str | None = Field(default=None, alias="Группа свариваемого материала")
    welding_materials: str | None = Field(default=None, alias="Сварочные материалы")
    details_thikness: str | None = Field(default=None, alias="Толщина деталей, мм")
    outer_diameter: str | None = Field(default=None, alias="Наружный диаметр, мм")
    welding_position: str | None = Field(default=None, alias="Положение при сварке")
    connection_type: str | None = Field(default=None, alias="Вид соединения")
    rod_diameter: str | None = Field(default=None, alias="Диаметр стержня, мм")
    rod_axis_position: str | None = Field(default=None, alias="Положение осей стержней")
    weld_type: str | None = Field(default=None, alias="Тип сварного соединения")
    joint_layer: str | None = Field(default=None, alias="Слой шва")
    gtd: str | None = Field(default=None, alias="Группы технических устройств опасных производственных объектов:")
    sdr: str | None = Field(default=None, alias="SDR")
    automation_level: str | None = Field( default=None, alias="Степень автоматизации")
    details_diameter: str | None = Field(default=None, alias="Диаметр деталей, мм")
    welding_equipment: str | None = Field(default=None, alias="Сварочное оборудование")
    certification_id : str | None = None

    model_config = ConfigDict(
        from_attributes=True,
        populate_by_name=True
    )
