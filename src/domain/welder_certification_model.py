from datetime import date, datetime
from re import fullmatch

from pydantic import ConfigDict, Field, field_validator

from src.db.db_tables import WelderCertificationTable
from src.domain.base_domain_model import BaseDomainModel


class WelderCertificationModel(BaseDomainModel):
    __table_model__ = WelderCertificationTable
    kleymo: str | None = Field(default=None)
    certification_id: str = Field(default=None)
    job_title: str = Field(default=None)
    certification_number: str = Field(default=None)
    certification_date: date | str = Field(default=None)
    expiration_date: date | str | None = Field(default=None)
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
        populate_by_name=True,
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
    def validate_date(cls, v: date | str | None) -> str | None:
        if type(v) == date: 
            return v
        
        if v == None:
            return None
        
        if fullmatch(r"([0-9]{4}[./-][0-9]{2}[./-][0-9]{2})|([0-9]{2}[./-][0-9]{2}[./-][0-9]{4})", v.strip()):
            return datetime.strptime(v.strip(), "%Y-%m-%d").date()
        
        raise ValueError("Invalid date")