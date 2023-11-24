from datetime import date
from re import fullmatch

from pydantic import Field, field_validator

from src.db.db_tables import WelderTable
from src.domain.base_domain_model import BaseDomainModel
from src.domain.welder_certification_model import WelderCertificationModel


class WelderModel(BaseDomainModel):
    __table_model__ = WelderTable
    kleymo: str = Field(max_length=150)
    full_name: str | None  = Field(max_length=150, default=None)
    birthday: str | date | None  = Field(max_length=150, default=None)
    passport_id: str | None = Field(max_length=150, default=None)
    certifications: list["WelderCertificationModel"] | None = Field(max_length=150, default=None)


    @field_validator("kleymo")
    def validate_kleymo(cls, v: str):
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v
        
        raise ValueError(f"Invalid kleymo: {v}")
    

    def __eq__(self, __value: "WelderModel") -> bool:
        if not super().__eq__(__value):
            return False
        
        if len(__value.certifications) != len(self.certifications):
            return False
        
        for i in range(len(self.certifications)):
            if self.certifications[i] != __value.certifications[i]:
                return False
            
        return True