from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, TypeAlias, Sequence, Literal

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.sql.elements import BinaryExpression
from sqlalchemy import or_, select, desc, update

from src.db.db_tables import NDTSummaryTable, NDTTable, WelderCertificationTable, WelderTable, Table
from src.db.engine import engine
from src.domain import (
    WelderModel, 
    NDTModel, 
    WelderCertificationModel, 
    DBRequest, 
    DBResponse, 
    WelderRequest,
    NDTRequest, 
    Model, 
    Count, 
    Name
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
    __tabledomain__: Model
    session = Session(engine)


    def get(self, id: Id) -> Model:
        return self.session.query(self.__tablemodel__).get(id)


    @abstractmethod
    def get(self, request: Request) -> DBResponse: ...


    @abstractmethod
    def _add(self, model: Model) -> None: ...


    @abstractmethod
    def add(self, data: Sequence[Model]) -> None: ...


    @abstractmethod
    def _update(self, model: Model) -> None: ...


    @abstractmethod
    def update(self, data: Sequence[Model]) -> None: ...


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


    def get(self, request: NDTRequest) -> DBResponse:
        ...

    
    def add(self, certifications: Sequence[WelderCertificationModel]) -> Sequence[WelderCertificationModel]:
        for certification in certifications:
            self._add(certification)


    def _add(self, certification: WelderCertificationModel) -> None:

        with self.session.begin_nested() as transaction:
            try:
                self.session.add(certification.to_orm())

                transaction.commit()
            
                print(f"welder with kleymo {certification.certification_id} successfully appended to {self.__tablename__}")

            except IntegrityError:
                print(f"ndt with id: {certification.certification_id} already exists")
                transaction.rollback()


    def update(self, certifications: Sequence[WelderCertificationModel]) -> None:
        for certification in certifications:
            self._update(certification)


    def _update(self, certification: WelderCertificationModel) -> None:

        with self.session.begin_nested() as transaction:
            try:
                stmt = update(WelderCertificationTable).where(
                    WelderCertificationTable.certification_id == certification.certification_id
                ).values(**certification.__dict__)

                self.session.execute(stmt)

                transaction.commit()
            
                print(f"welder certification with id {certification.certification_id} successfully updated")

            except IntegrityError as e:
                print(f"certification has not been updated")
                print(e)
                transaction.rollback()


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository):
    __tablename__ = "welder_table"
    __tablemodel__ = WelderTable
    certification_repository = WelderCertificationRepository()


    def get(self, request: WelderRequest) -> DBResponse:
        ...

    
    def add(self, welders: Sequence[WelderModel]) -> Sequence[WelderModel]:
        for welder in welders:
            self._add(welder)

        
    def update(self, welders: Sequence[NDTModel]) -> None:
        for welder in welders:
            self._update(welder)


    def _add(self, welder: WelderModel) -> None:
        self.certification_repository.add(welder.certifications)

        with self.session.begin_nested() as transaction:
            try:
                self.session.add(welder.to_orm())

                transaction.commit()
            
                print(f"welder with kleymo {welder.kleymo} successfully appended to {self.__tablename__}")

            except IntegrityError:
                print(f"ndt with id: {welder.kleymo} already exists")
                transaction.rollback()


    def _update(self, welder: WelderModel) -> None:
        certifications = welder.certifications

        self.certification_repository.update(certifications)

        with self.session.begin_nested() as transaction:
            try:
                stmt = update(WelderTable).where(
                    WelderTable.kleymo == welder.kleymo
                ).values(**welder.__dict__)

                self.session.execute(stmt)

                transaction.commit()
            
                print(f"welder {welder.full_name} ({welder.kleymo}) successfully updated")

            except IntegrityError as e:
                print(f"welder {welder.full_name} ({welder.kleymo}) has not been updated")
                print(e)
                transaction.rollback()


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


    def get(self, request: NDTRequest) -> DBResponse[NDTModel]:
        self.request = request
        self._get_expressions()

        stmt = select(self.__tablemodel__, WelderTable.full_name)\
            .join(WelderTable, self.__tablemodel__.kleymo == WelderTable.kleymo)\
            .join(WelderCertificationTable, self.__tablemodel__.kleymo == WelderCertificationTable.kleymo)\
            .filter(or_(*self.search_expressions), *self.filter_expressions).distinct()\
            .order_by(desc(self.__tablemodel__.latest_welding_date))
        

        conn = self.session.connection()

        res = conn.execute(stmt).mappings().all()
        
        
        return DBResponse(
            count = len(res),
            result = [
                NDTModel.model_validate(ndt) for ndt in res
            ]
        )


    def add(self, ndts: Sequence[NDTModel]) -> NDTModel:
        for ndt in ndts:
            self._add(ndt)

    
    def update(self, ndts: Sequence[NDTModel]) -> None:
        for ndt in ndts:
            self._update(ndt)


    def _update(self, ndt: NDTModel) -> None:
        with self.session.begin_nested() as transaction:
            try:
                stmt = update(self.__tablemodel__).where(
                    self.__tablemodel__.ndt_id == ndt.ndt_id
                ).values(**ndt.__dict__)

                self.session.execute(stmt)

                transaction.commit()
            
                print(f"ndt with id {ndt.kleymo} successfully updated")

            except IntegrityError as e:
                print(f"ndt with id {ndt.kleymo} has not been updated")
                print(e)
                transaction.rollback()


    def _add(self, ndt: NDTModel) -> None:

        with self.session.begin_nested() as transaction:
            try:
                self.session.add(ndt.to_orm())

                transaction.commit()
            
                print(f"ndt with id {ndt.kleymo} successfully appended")

            except IntegrityError as e:
                print(f"ndt with id {ndt.kleymo} has not been appended")
                transaction.rollback()


    def _get_expressions(self) -> None:
        self.search_expressions: list[BinaryExpression] = []
        self.filter_expressions: list[BinaryExpression] = []

        self._get_kleymo_expression()
        self._get_names_expression()
        self._get_certification_number_expression()
        self._get_comp_expression()
        self._get_subcomp_expression()
        self._get_project_expression()
        self._get_date_expression()

    
    def _get_kleymo_expression(self) -> None:

        if self.request.kleymos != None:
            self.search_expressions.append(self.__tablemodel__.kleymo.in_(self.request.kleymos))
    

    def _get_names_expression(self) -> None:
        
        if self.request.names != None:
            self.search_expressions.append(WelderTable.full_name.in_(self.request.names))


    def _get_certification_number_expression(self) -> None:
        
        if self.request.certification_numbers != None:
            self.search_expressions.append(WelderCertificationTable.certification_number.in_(self.request.certification_numbers))

    
    def _get_comp_expression(self) -> None:
        
        if self.request.comps != None:
            self.filter_expressions.append(self.__tablemodel__.comp.in_(self.request.comps))

    def _get_subcomp_expression(self) -> None:
        
        if self.request.subcomps != None:
            self.filter_expressions.append(self.__tablemodel__.subcon.in_(self.request.subcomps))

    def _get_project_expression(self) -> None:
        
        if self.request.projects != None:
            self.filter_expressions.append(self.__tablemodel__.project.in_(self.request.projects))
    

    def _get_date_expression(self) -> None:
        
        if self.request.date_before != None:
            self.filter_expressions.append(self.__tablemodel__.latest_welding_date <= self.request.date_before)

        if self.request.date_from != None:
            self.filter_expressions.append(self.__tablemodel__.latest_welding_date >= self.request.date_from)
