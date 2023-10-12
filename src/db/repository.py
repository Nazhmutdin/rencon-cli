from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, TypeAlias, Sequence, Literal

from sqlalchemy.orm import Session

from db.db_tables import NDTSummaryTable, NDTTable, WelderCertificationTable, WelderTable
from domain.value_objects import DBRequest, DBResponse, WelderRequest, NDTRequest , Model, Count, Name
from domain.domain_models import WelderModel, NDTModel, WelderCertificationModel


"""
=======================================================================================================
Types
=======================================================================================================
"""


Table = TypeVar("Table", bound=Union[NDTSummaryTable, NDTTable, WelderCertificationTable, WelderTable])
Request = TypeVar("Request", DBRequest)
Id: TypeAlias = Union[str, float, int]


"""
=======================================================================================================
Abstract Repository
=======================================================================================================
"""


class Repository(metaclass=ABCMeta):
    __tablename__: Name
    __tablemodel__: Table
    session = Session(__tablemodel__)

    @abstractmethod
    def get(self, id: Id) -> Model: ...


    @abstractmethod
    def list(self, request: Request) -> DBResponse: ...


    @abstractmethod
    def _add(self, model: Model) -> None: ...


    @abstractmethod
    def add(self, data: Sequence[Model]) -> Model: ...


    @property
    def count(self) -> Count:
        return self.session.query(self.__tablemodel__).count()


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(Repository):
    __tablename__ = "welder_table"
    __tablemodel__ = WelderTable

    def get(self, id: Id) -> WelderModel:
        self.session.query(self.__tablemodel__).get(id)


    def list(self, request: WelderRequest) -> DBResponse:
        ...

    
    def add(self, data: Sequence[WelderModel]) -> Sequence[WelderModel]:
        ...


    def _add(self, model: WelderModel) -> None:
        ...


"""
=======================================================================================================
Welder's Certification Repository
=======================================================================================================
"""


class WelderCertificationRepository(Repository):
    __tablename__ = "welder_certification_table"
    __tablemodel__ = WelderCertificationTable

    def get(self, id: Id) -> WelderCertificationModel:
        self.session.query(self.__tablemodel__).get(id)


    def list(self, request: Request) -> DBResponse:
        ...

    
    def add(self, data: Sequence[WelderCertificationModel]) -> Sequence[WelderCertificationModel]:
        ...


    def _add(self, model: WelderCertificationModel) -> None:
        ...


"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(Repository):

    def __init__(self, table_name: Literal["ndt_table",  "ndt_summary_table"]) -> None:

        if table_name not in ["ndt_table",  "ndt_summary_table"]:
            raise ValueError("This repository accept only 'ndt_table',  'ndt_summary_table'")

        match table_name:
            case "ndt_table":
                self.__tablename__ = "ndt_table"
                self.__tablemodel__ = NDTTable
            
            case "ndt_summary_table":
                self.__tablename__ = "ndt_summary_table"
                self.__tablemodel__ = NDTSummaryTable


    def get(self, id: Id) -> NDTModel:
        self.session.query(self.__tablemodel__).get(id)


    def list(self, request: Request) -> DBResponse:
        ...

    
    def add(self, data: Sequence[NDTModel]) -> NDTModel:
        ...


    def _add(self, model: NDTModel) -> None:
       ...
