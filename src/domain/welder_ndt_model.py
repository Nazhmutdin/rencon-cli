from datetime import date
from re import fullmatch, sub

from pydantic import Field, field_validator

from src.db.db_tables import  NDTTable
from src.domain.base_domain_model import BaseDomainModel


class WelderNDTModel(BaseDomainModel):
    __table_model__ = NDTTable
    full_name: str | None = Field(default=None)
    sicil_number: str | int | None = Field(default=None)
    kleymo: str | int = Field(default=None)
    birthday: date | None = Field(default=None)
    passport_number: str | int | None = Field(default=None)
    nation: str | None = Field(default=None)
    comp: str | None = Field(default=None)
    subcon: str | None = Field(default=None)
    project: str | None = Field(default=None)
    latest_welding_date: date = Field(default=None)
    total_weld_1: float | None = Field(default=None)
    total_ndt_1: float | None = Field(default=None)
    total_accepted_1: float | None = Field(default=None)
    total_repair_1: float | None = Field(default=None)
    repair_status_1: float | None = Field(default=None)
    total_weld_2: float | None = Field(default=None)
    total_ndt_2: float | None = Field(default=None)
    total_accepted_2: float | None = Field(default=None)
    total_repair_2: float | None = Field(default=None)
    repair_status_2: float | None = Field(default=None)
    total_weld_3: float | None = Field(default=None)
    total_ndt_3: float | None = Field(default=None)
    total_accepted_3: float | None = Field(default=None)
    total_repair_3: float | None = Field(default=None)
    repair_status_3: float | None = Field(default=None)
    ndt_id: str = Field(default=None)


    def set_id(self) -> None:
        self.ndt_id = sub(
            r"\W",
            "",
            string=f"{self.kleymo}{self.comp}{self.subcon}{self.project}{self.latest_welding_date.strftime("%Y-%m-%d")}".lower()
        )


    @field_validator("latest_welding_date")
    def validate_latest_welding_date(cls, v):
        if type(v) != date or v == None:
            raise ValueError("latest_welding_date must be date type")
        
        return v


    @field_validator("kleymo")
    def validate_kleymo(cls, v) -> str:
        if not fullmatch(r"[A-Z0-9]{4}", str(v).strip()) or v == None:
            raise ValueError(f"Invalid kleymo ===> {v}")
        
        return str(v).strip()
