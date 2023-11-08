from abc import ABCMeta, abstractmethod
from typing import TypeVar, Union, TypeAlias, Sequence

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, insert

from src.db.db_tables import NDTSummaryTable, WelderCertificationTable, WelderTable, Table
from src.db.session import get_session
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
Unit of Work
=======================================================================================================
"""


class SQLalchemyUnitOfWork:
    def __enter__(self):
        self.session = get_session()

        return self


    def __exit__(self):
        self.session.close()

    
    def commit(self) -> None:
        self.session.commit()


    def rollback(self) -> None:
        self.session.rollback()


"""
=======================================================================================================
Abstract Repository
=======================================================================================================
"""


class BaseRepository(metaclass=ABCMeta):
    __tablemodel__: Table


    def get(self, id: Id) -> Model:
        session = get_session()
        result = session.query(self.__tablemodel__).get(id)
        session.close()

        return result


    @abstractmethod
    def get_many(self, request: Request) -> DBResponse: ...


    @abstractmethod
    def add(self, data: Sequence[Model]) -> None: ...


    @abstractmethod
    def update(self, data: Sequence[Model]) -> None: ...


    @abstractmethod
    def delete(self, data: Sequence[Model]) -> None: ...


    def _add(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(self.__tablemodel__).values(**model.model_dump())
                transaction.session.execute(stmt)

                transaction.commit()

            except IntegrityError:
                transaction.rollback()

    
    def _update(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(self.__tablemodel__).values(**model.__dict__)
                transaction.session.execute(stmt)

                transaction.commit()

            except IntegrityError:
                transaction.rollback()


    @property
    def count(self) -> Count:
        session = get_session()
        result = session.query(self.__tablemodel__).count()
        session.close()

        return result


"""
=======================================================================================================
Welder's Certification Repository
=======================================================================================================
"""


class WelderCertificationRepository(BaseRepository):
    __tablemodel__: WelderCertificationTable = WelderCertificationTable

    def get_many(self, request: NDTRequest) -> DBResponse:
        ...

    
    def add(self, certifications: Sequence[WelderCertificationModel]) -> Sequence[WelderCertificationModel]:
        for certification in certifications:
            self._add(certification)


    def update(self, certifications: Sequence[WelderCertificationModel]) -> None:
        for certification in certifications:
            self._update(certification)


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository):
    __tablemodel__: WelderTable = WelderTable
    certification_repository = WelderCertificationRepository()

    def get_many(self, request: WelderRequest) -> DBResponse:
        ...

    
    def add(self, welders: Sequence[WelderModel]) -> Sequence[WelderModel]:
        for welder in welders:
            self._add(welder)

        
    def update(self, welders: Sequence[NDTModel]) -> None:
        for welder in welders:
            self._update(welder)


    def _add(self, welder: WelderModel) -> None:
        self.certification_repository.add(welder.certifications)

        super()._add(welder)


    def _update(self, welder: WelderModel) -> None:
        self.certification_repository.update(welder.certifications)

        super()._update(welder)


"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(BaseRepository):
    __tablemodel__: NDTSummaryTable = NDTSummaryTable

    def get_many(self, request: NDTRequest) -> DBResponse[NDTModel]: ...

        # stmt = select(self.__tablemodel__, WelderTable.full_name)\
        #     .join(WelderTable, self.__tablemodel__.kleymo == WelderTable.kleymo)\
        #     .join(WelderCertificationTable, self.__tablemodel__.kleymo == WelderCertificationTable.kleymo)\
        #     .filter(or_(*self.search_expressions), *self.filter_expressions).distinct()\
        #     .order_by(desc(self.__tablemodel__.latest_welding_date))

        # res = conn.execute(stmt).mappings().all()


    def add(self, ndts: Sequence[NDTModel]) -> NDTModel:
        for ndt in ndts:
            self._add(ndt)

    
    def update(self, ndts: Sequence[NDTModel]) -> None:
        for ndt in ndts:
            self._update(ndt)
