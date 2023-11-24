from typing import Any

from pydantic import BaseModel

from src.db.session import Base


class BaseDomainModel[Table: Base, Model: "BaseDomainModel"](BaseModel):
    __table_model__: Table

    @property
    def orm_data(self) -> dict[str, Any]:
        table_keys = list(self.__table_model__.__table__.c.keys())
        model_data = self.model_dump()
        
        return {key: model_data[key] for key in table_keys}
    

    def __eq__(self, __value: Model) -> bool:
        if not isinstance(__value, type(self)):
            return False
        
        self_dict = self.model_dump()

        for key, value in __value.model_dump().items():
            if key not in self_dict:
                return False
            
            if value != self_dict[key]:
                return False
        
        return True
