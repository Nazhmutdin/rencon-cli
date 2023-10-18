from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, TypeAlias, Sequence, Literal, Generic

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import Select, and_, or_, select

from src.db.db_tables import NDTSummaryTable, NDTTable, WelderCertificationTable, WelderTable
from src.db.engine import engine
from src.domain import (
    WelderModel, 
    NDTModel, 
    WelderCertificationModel, 
    DBRequest, 
    DBResponse, 
    WelderRequest,
    NDTRequest, 
    DomainModel, 
    Count, 
    Name,
    Kleymo,
    CertificationNumber,
    Table
)


"""
=======================================================================================================
Types
=======================================================================================================
"""


Request = TypeVar("Request", bound=DBRequest)
Repository = TypeVar("Repository", bound="BaseRepository")
Id: TypeAlias = Union[str, float, int]


"""
=======================================================================================================
Abstract Repository
=======================================================================================================
"""


class BaseRepository(metaclass=ABCMeta):
    __tablename__: Name
    __tablemodel__: Table
    __tabledomain__: DomainModel
    session = Session(engine)


    def get(self, id: Id) -> DomainModel:
        return self.session.query(self.__tablemodel__).get(id)


    @abstractmethod
    def get_by_request(self, request: Request) -> DBResponse: ...


    @abstractmethod
    def _add(self, model: DomainModel) -> None: ...


    @abstractmethod
    def add(self, data: Sequence[DomainModel]) -> None: ...


    @abstractmethod
    def _update(self, model: DomainModel) -> None: ...


    @abstractmethod
    def update(self, data: Sequence[DomainModel]) -> None: ...


    @property
    def count(self) -> Count:
        return self.session.query(self.__tablemodel__).count()


"""
=======================================================================================================
Welder's Certification Repository
=======================================================================================================
"""


class WelderCertificationRepository(BaseRepository):
    __tablename__ = "welder_certification_table"
    __tablemodel__ = WelderCertificationTable


    def get_by_request(self, request: NDTRequest) -> DBResponse:
        ...

    
    def add(self, certifications: Sequence[WelderCertificationModel]) -> Sequence[WelderCertificationModel]:
        for certification in certifications:
            self._add(certification)


    def _add(self, certification: WelderCertificationModel) -> None:
        certification_orm = certification.convert_to_orm_model()

        with self.session.begin_nested() as transaction:
            try:
                self.session.add(certification_orm)

                transaction.commit()
            
                print(f"welder with kleymo {certification.certification_id} successfully appended to {self.__tablename__}")

            except IntegrityError:
                print(f"ndt with id: {certification.certification_id} already exists")
                transaction.rollback()
    

    def update(self, ndts: Sequence[NDTModel]) -> None: ...


    def _update(self, ndt: DomainModel) -> None: ...




"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository):
    __tablename__ = "welder_table"
    __tablemodel__ = WelderTable
    certification_repository = WelderCertificationRepository()


    def get_by_request(self, request: WelderRequest) -> DBResponse:
        ...

    
    def add(self, welders: Sequence[WelderModel]) -> Sequence[WelderModel]:
        for welder in welders:
            self._add(welder)


    def _add(self, welder: WelderModel) -> None:
        welder_orm = welder.to_orm()
        self.certification_repository.add(welder.certifications)

        with self.session.begin_nested() as transaction:
            try:
                self.session.add(welder_orm)

                transaction.commit()
            
                print(f"welder with kleymo {welder.kleymo} successfully appended to {self.__tablename__}")

            except IntegrityError:
                print(f"ndt with id: {welder.kleymo} already exists")
                transaction.rollback()

        
    def update(self, ndts: Sequence[NDTModel]) -> None: ...


    def _update(self, ndt: DomainModel) -> None: ...




"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(BaseRepository):

    def __init__(self, table_name: Literal["ndt_table",  "ndt_summary_table"]) -> None:

        if table_name not in ["ndt_table",  "ndt_summary_table"]:
            raise ValueError("This repository accept only 'ndt_table',  'ndt_summary_table'")

        match table_name:
            case "ndt_table":
                self.__tablename__ = "ndt_table"
                self.__tablemodel__: NDTTable  = NDTTable
            
            case "ndt_summary_table":
                self.__tablename__ = "ndt_summary_table"
                self.__tablemodel__: NDTSummaryTable = NDTSummaryTable


    def get_by_request(self, request: NDTRequest) -> DBResponse[NDTModel]:
        expressions: list[BinaryExpression] = []

        self._get_kleymo_filter(request.kleymos, expressions)
        self._get_names_filter(request.names, expressions)
        self._get_certification_number_filter(request.certification_numbers, expressions)

        res = self.session.query(self.__tablemodel__)\
            .join(WelderTable, self.__tablemodel__.kleymo == WelderTable.kleymo)\
            .join(WelderCertificationTable, self.__tablemodel__.kleymo == WelderCertificationTable.kleymo)\
            .filter(or_(*expressions)).order_by(self.__tablemodel__.latest_welding_date)
        
        return DBResponse(
            count = res.count(),
            summary_count = res.count(),
            result = [
                NDTModel.model_validate(ndt) for ndt in res.all()
            ]
        )


    def add(self, ndts: Sequence[NDTModel]) -> NDTModel: ... 

    
    def update(self, ndts: Sequence[NDTModel]) -> None: ...


    def _update(self, ndt: DomainModel) -> None: ...


    def _add(self, ndt: NDTModel) -> None: ...

    
    def _get_kleymo_filter(self, kleymos: Sequence[Kleymo], expressions: list[BinaryExpression]) -> None:

        if kleymos != None:
            expressions.append(self.__tablemodel__.kleymo.in_(kleymos))
    

    def _get_names_filter(self, names: Sequence[Name], expressions: list[BinaryExpression]) -> None:
        
        if names != None:
            expressions.append(WelderTable.full_name.in_(names))


    def _get_certification_number_filter(self, certification_numbers: Sequence[CertificationNumber], expressions: list[BinaryExpression]) -> None:
        
        if certification_numbers != None:
            expressions.append(WelderCertificationTable.certification_number.in_(certification_numbers))
