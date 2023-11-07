from typing import TypeAlias, Union, Sequence, TypeVar, Generic
from datetime import date, datetime
from re import fullmatch

from pydantic import BaseModel, ConfigDict, Field, field_validator


"""
=======================================================================================================
Types
=======================================================================================================
"""


Limit: TypeAlias = int
Offset: TypeAlias = int
Name: TypeAlias = str
Kleymo: TypeAlias = str
CertificationNumber: TypeAlias = str
Company: TypeAlias = str
SubCompany: TypeAlias = str
Project: TypeAlias = str
DateFrom: TypeAlias = str
DateBefore: TypeAlias = str
Count: TypeAlias = int
Model = TypeVar("Model", bound=BaseModel)


"""
=======================================================================================================
NDT Model
=======================================================================================================
"""


class NDTModel(BaseModel):
    full_name: str | None = Field(default=None)
    kleymo: str | int = Field(default=None)
    sicil_number: str | None = Field(default=None)
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


"""
=======================================================================================================
Welder Model
=======================================================================================================
"""


class WelderModel(BaseModel):
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


"""
=======================================================================================================
Welder's Certification Model
=======================================================================================================
"""


class WelderCertificationModel(BaseModel):
    kleymo: str | None = Field(default=None)
    certification_id: str = Field(default=None)
    job_title: str = Field(default=None)
    certification_number: str = Field(default=None)
    certification_date: date | str = Field(default=None)
    expiration_date: date | str = Field(default=None)
    renewal_date: date | str | None = Field(default=None)
    insert: str = Field(default=None)
    certification_type: str | None = Field(default=None)
    company: str | None = Field(default=None, alias="Место работы (организация, инн):")
    gtd: str | None = Field(default=None, alias="Группы технических устройств опасных производственных объектов:")
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
    sdr: str | None = Field(default=None, alias="SDR")
    automation_level: str | None = Field( default=None, alias="Степень автоматизации")
    details_diameter: str | None = Field(default=None, alias="Диаметр деталей, мм")
    welding_equipment: str | None = Field(default=None, alias="Сварочное оборудование")


    model_config = ConfigDict(
        populate_by_name=True
    )


    @property
    def alias_to_field_ref(cls) -> dict[str, str]:
        field_dict: dict[str, str] = {}

        for key, value in cls.model_fields.items():
            if value.alias != None:
                field_dict.update(
                    {
                        value.alias: key
                    }
                )
        
        return field_dict
    
    
    def set_field_by_alias(self, alias: str, value: str) -> None:
        try:
            self.__dict__[self.alias_to_field_ref[alias]] = value
        except KeyError:
            raise KeyError("Invalid key: %s" % (alias))
        

    @field_validator("kleymo")
    def validate_kleymo(cls, v: str) -> str:
        if v == None:
            return None
        
        if fullmatch(r"[A-Z0-9]{4}", v.strip()):
            return v.strip()
        
        raise ValueError(f"Invalid kleymo ===> {v}")
    

    @field_validator("certification_date", "expiration_date")
    def validate_date(cls, v: date| str) -> str | None:
        if type(v) == date: 
            return v
        
        if fullmatch(r"([0-9]{4}[./-][0-9]{2}[./-][0-9]{2})|([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})", v.strip()):
            return datetime.strptime(v.strip(), "%Y-%m-%d").date()
        
        raise ValueError("Invalid date")



"""
=======================================================================================================
value objects
=======================================================================================================
"""


class DBRequest(BaseModel):
    limit: Union[Limit, None] = None
    offset: Union[Offset, None] = None


class WelderRequest(DBRequest):
    names: Union[Sequence[Name], None] = None
    kleymos: Union[Sequence[Kleymo], None] = None
    certification_numbers: Union[Sequence[CertificationNumber], None] = None


class NDTRequest(DBRequest):
    names: Union[Sequence[Name], None] = None
    kleymos: Union[Sequence[Kleymo], None] = None
    certification_numbers: Union[Sequence[CertificationNumber], None] = None
    comps: Union[Sequence[Company], None] = None
    subcomps: Union[Sequence[SubCompany], None] = None
    projects: Union[Sequence[Project], None] = None
    date_from: Union[DateFrom, None] = None
    date_before: Union[DateBefore, None] = None


class DBResponse(BaseModel, Generic[Model]):
    count: Count
    result: Sequence[Model]
