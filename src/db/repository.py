from abc import ABC, abstractmethod
from typing import TypeVar, Union, TypeAlias

from sqlalchemy.exc import IntegrityError
from sqlalchemy import update, insert, delete, inspect, select
from sqlalchemy.orm import subqueryload
from sqlalchemy.sql.schema import Column

from src.db.db_tables import NDTTable, WelderCertificationTable, WelderTable, Table
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


    def __exit__(self, exception_type, exception_value, traceback):
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


class BaseRepository(ABC):
    __tablemodel__: Table
    __domain_model__: Model


    def get(self, id: Id) -> Model | None:
        session = get_session()
        stmt = select(self.__tablemodel__).where(
            self.pk == id
        )

        result = session.execute(stmt).fetchone()
        if result == None:
            session.close()
            return None
        
        session.close()

        return self.__domain_model__.model_validate(result[0], from_attributes=True)


    @abstractmethod
    def get_many(self, request: Request) -> DBResponse: ...


    def add(self, data: list[Model]) -> None:
        
        for model in data:
            self._add(model)


    def update(self, data: list[Model]) -> None:
        
        for model in data:
            self._update(model)


    def delete(self, data: list[Model]) -> None:
        
        for model in data:
            self._delete(model)


    def _add(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(self.__tablemodel__).values(**model.orm_data)

                transaction.session.execute(stmt)

                transaction.commit()

            except IntegrityError:
                transaction.rollback()


    def _update(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(self.__tablemodel__).where(
                    self.pk == getattr(model, self.pk.name)
                ).values(**model.orm_data)
                transaction.session.execute(stmt)

                transaction.commit()

            except IntegrityError:
                transaction.rollback()


    def _delete(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = delete(self.__tablemodel__).where(
                    self.pk == getattr(model, self.pk.name)
                )
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
    

    @property
    def pk(self) -> Column:
        return inspect(self.__tablemodel__).primary_key[0]


"""
=======================================================================================================
Welder's Certification Repository
=======================================================================================================
"""


class WelderCertificationRepository(BaseRepository):
    __tablemodel__: WelderCertificationTable = WelderCertificationTable
    __domain_model__: Model = WelderCertificationModel

    def get_many(self, request: NDTRequest) -> DBResponse:
        ...


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository):
    __tablemodel__: WelderTable = WelderTable
    __domain_model__: Model = WelderModel
    certification_repository = WelderCertificationRepository()


    def get(self, id: Id) -> Model | None:
        session = get_session()
        stmt = select(self.__tablemodel__).where(
            self.pk == id
        ).options(
            subqueryload(WelderTable.certifications)
        )

        result = session.execute(stmt).fetchone()
        if result == None:
            session.close()
            return None
        
        session.close()

        welder = self.__domain_model__.model_validate(result[0], from_attributes=True)
        print(len(welder.certifications))

        return welder


    def get_many(self, request: WelderRequest) -> DBResponse:
        ...

    
    def add(self, welders: list[WelderModel]) -> None:
        for welder in welders:
            self._add(welder)
            self.certification_repository.add(welder.certifications)

        
    def update(self, welders: list[NDTModel]) -> None:
        for welder in welders:
            self.certification_repository.update(welder.certifications)
            self._update(welder)


    def delete(self, welders: list[WelderModel]) -> None:
        for welder in welders:
            self.certification_repository.delete(welder.certifications)
            self._delete(welder)


"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(BaseRepository):
    __tablemodel__: NDTTable = NDTTable
    __domain_model__: Model = NDTModel

    def get_many(self, request: NDTRequest) -> DBResponse[NDTModel]: ...

        # stmt = select(self.__tablemodel__, WelderTable.full_name)\
        #     .join(WelderTable, self.__tablemodel__.kleymo == WelderTable.kleymo)\
        #     .join(WelderCertificationTable, self.__tablemodel__.kleymo == WelderCertificationTable.kleymo)\
        #     .filter(or_(*self.search_expressions), *self.filter_expressions).distinct()\
        #     .order_by(desc(self.__tablemodel__.latest_welding_date))

        # res = conn.execute(stmt).mappings().all()

