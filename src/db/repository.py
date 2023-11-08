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

    def get_many(self, request: NDTRequest) -> DBResponse:
        ...

    
    def add(self, certifications: Sequence[WelderCertificationModel]) -> Sequence[WelderCertificationModel]:
        for certification in certifications:
            self._add(certification)


    def update(self, certifications: Sequence[WelderCertificationModel]) -> None:
        for certification in certifications:
            self._update(certification)


    def _add(self, certification: WelderCertificationModel) -> None:

        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(WelderCertificationTable).values(**certification.model_dump())
                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"welder with kleymo {certification.certification_id} successfully appended")

            except IntegrityError:
                print(f"ndt with id: {certification.certification_id} already exists")
                transaction.rollback()


    def _update(self, certification: WelderCertificationModel) -> None:

        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(WelderCertificationTable).where(
                    WelderCertificationTable.certification_id == certification.certification_id
                ).values(**certification.model_dump())

                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"welder certification with id {certification.certification_id} successfully updated")

            except IntegrityError:
                print(f"certification has not been updated")
                transaction.rollback()


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository):
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

        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(WelderTable).values(**welder.model_dump())
                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"welder with kleymo {welder.kleymo} successfully appended")

            except IntegrityError:
                print(f"ndt with id: {welder.kleymo} already exists")
                transaction.rollback()


    def _update(self, welder: WelderModel) -> None:
        certifications = welder.certifications

        self.certification_repository.update(certifications)

        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(WelderTable).where(
                    WelderTable.kleymo == welder.kleymo
                ).values(**welder.__dict__)

                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"welder {welder.full_name} ({welder.kleymo}) successfully updated")

            except IntegrityError:
                print(f"welder {welder.full_name} ({welder.kleymo}) has not been updated")
                transaction.rollback()


"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(BaseRepository):

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


    def _update(self, ndt: NDTModel) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(NDTSummaryTable).where(
                    NDTSummaryTable.ndt_id == ndt.ndt_id
                ).values(**ndt.__dict__)

                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"ndt with id {ndt.kleymo} successfully updated")

            except IntegrityError:
                print(f"ndt with id {ndt.kleymo} has not been updated")
                transaction.rollback()


    def _add(self, ndt: NDTModel) -> None:

        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = insert(NDTSummaryTable).values(**ndt.model_dump())
                transaction.session.execute(stmt)

                transaction.commit()
            
                print(f"ndt with id {ndt.kleymo} successfully appended")

            except IntegrityError:
                print(f"ndt with id {ndt.kleymo} has not been appended")
                transaction.rollback()
