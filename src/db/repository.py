from abc import ABC, abstractmethod
from typing import TypeVar, Union, TypeAlias

from sqlalchemy.exc import IntegrityError
from sqlalchemy import Select, event, update, insert, delete, inspect, select, desc
from sqlalchemy.orm import subqueryload
from sqlalchemy.sql.schema import Column

from src.db.db_tables import NDTTable, WelderCertificationTable, WelderTable
from src.db.session import Base, get_session
from src.domain import (
    WelderModel,
    WelderNDTModel,
    WelderCertificationModel,
    WelderCertificationRequest,
    BaseDomainModel,
    DBRequest,
    DBResponse,
    WelderRequest,
    NDTRequest
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
        self.connection = self.session.connection()
        self.engine = self.connection.engine
        self.count = 0

        event.listen(self.engine, "before_cursor_execute", self.callback)

        return self


    def __exit__(self, *args, **kwargs):
        event.remove(self.engine, "before_cursor_execute", self.callback)

    
    def commit(self) -> None:
        self.session.commit()


    def rollback(self) -> None:
        self.session.rollback()


    def callback(self, *args, **kwargs) -> None:
        self.count += 1


"""
=======================================================================================================
Abstract Repository
=======================================================================================================
"""


class BaseRepository[Model: BaseDomainModel, Table: Base](ABC):
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

                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                if "UniqueViolation" not in e.args[0]:
                    print(e)
                    
                transaction.rollback()


    def _update(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = update(self.__tablemodel__).where(
                    self.pk == getattr(model, self.pk.name)
                ).values(**model.orm_data)

                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                print(e)
                transaction.rollback()


    def _delete(self, model: Model) -> None:
        with SQLalchemyUnitOfWork() as transaction:
            try:
                stmt = delete(self.__tablemodel__).where(
                    self.pk == getattr(model, self.pk.name)
                )
                
                transaction.connection.execute(stmt)

                transaction.commit()

            except IntegrityError as e:
                print(e)
                transaction.rollback()


    @property
    def count(self) -> int:
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


class WelderCertificationRepository(BaseRepository[WelderCertificationModel, WelderCertificationTable]):
    __tablemodel__ = WelderCertificationTable
    __domain_model__ = WelderCertificationModel

    def get_many(self, request: WelderCertificationRequest) -> DBResponse[WelderCertificationModel]:
        with SQLalchemyUnitOfWork() as transaction:
            stmt = self._filtrate_statement(select(self.__tablemodel__), request)

            res = transaction.connection.execute(stmt).mappings().all()

        return DBResponse(
            result=[WelderCertificationModel.model_validate(certification) for certification in res],
            count=5
        )

    
    def _filtrate_statement(self, stmt: Select, request: WelderCertificationRequest) -> Select:
        if request.expiration_date_before:
            stmt = stmt.filter(self.__tablemodel__.expiration_date < request.expiration_date_before)

        if request.expiration_date_from:
            stmt = stmt.filter(self.__tablemodel__.expiration_date > request.expiration_date_from)

        return stmt


"""
=======================================================================================================
Welder Repository
=======================================================================================================
"""


class WelderRepository(BaseRepository[WelderModel, WelderTable]):
    __tablemodel__ = WelderTable
    __domain_model__ = WelderModel
    certification_repository = WelderCertificationRepository()


    def get(self, id: Id) -> WelderModel | None:
        session = get_session()
        stmt = select(self.__tablemodel__).where(
            self.pk == id
        ).options(
            subqueryload(self.__tablemodel__.certifications)
        )

        result = session.execute(stmt).fetchone()
        if result == None:
            session.close()
            return None
        
        session.close()

        welder = self.__domain_model__.model_validate(result[0], from_attributes=True)

        return welder


    def get_many(self, request: WelderRequest) -> list[WelderModel]:
            
        with SQLalchemyUnitOfWork() as transaction:

            stmt = select(self.__tablemodel__).options(
                subqueryload(self.__tablemodel__.certifications)
            )

            stmt = self._get_many_filtrating(stmt, request)

            res = transaction.connection.execute(stmt)

        return [WelderModel.model_validate(welder, from_attributes=True) for welder in res.mappings().all()]


    def add(self, data: list[WelderModel]) -> None:
        for welder in data:
            self._add(welder)
            self.certification_repository.add(welder.certifications)

        
    def update(self, data: list[WelderModel]) -> None:
        for welder in data:
            self.certification_repository.update(welder.certifications)
            self._update(welder)


    def delete(self, data: list[WelderModel]) -> None:
        for welder in data:
            self.certification_repository.delete(welder.certifications)
            self._delete(welder)

    
    def _get_many_filtrating(self, select: Select, request: WelderRequest) -> Select:
        if request.names:
            select = select.filter(WelderTable.full_name.in_(request.names))

        if request.kleymos:
            select = select.filter(WelderTable.kleymo.in_(request.kleymos))

        return select



"""
=======================================================================================================
NDT Repository
=======================================================================================================
"""


class NDTRepository(BaseRepository[WelderNDTModel, NDTTable]):
    __tablemodel__ = NDTTable
    __domain_model__ = WelderNDTModel

    def get_many(self, request: NDTRequest) -> DBResponse[WelderNDTModel]:
        session = get_session()

        stmt = select(self.__tablemodel__, WelderTable.full_name, WelderCertificationTable.certification_number)\
            .join(WelderTable, self.__tablemodel__.kleymo == WelderTable.kleymo)\
            .join(WelderCertificationTable, self.__tablemodel__.kleymo == WelderCertificationTable.kleymo)\
            .order_by(desc(self.__tablemodel__.latest_welding_date))
        

        filtrated_stmt = self._set_filters(stmt, request)
        res = []

        for el in session.execute(filtrated_stmt).mappings().all():
            ndt_table_dict = el["NDTTable"].__dict__
            ndt_table_dict["full_name"] = el["full_name"]

            res.append(
                WelderNDTModel.model_validate(ndt_table_dict)
            )

        
        return DBResponse(
            result=res,
            count=len(list(session.execute(stmt)))
        )


    def _set_filters(self, stmt: Select, request: NDTRequest) -> Select:
        if request.kleymos:
            stmt = stmt.filter(self.__tablemodel__.kleymo.in_(request.kleymos))

        if request.comps:
            stmt = stmt.filter(self.__tablemodel__.comp.in_(request.comps))

        if request.subcomps:
            stmt = stmt.filter(self.__tablemodel__.subcon.in_(request.subcomps))

        if request.projects:
            stmt = stmt.filter(self.__tablemodel__.project.in_(request.projects))

        if request.date_before:
            stmt = stmt.filter(self.__tablemodel__.latest_welding_date <= request.date_before)

        if request.date_from:
            stmt = stmt.filter(self.__tablemodel__.latest_welding_date >= request.date_from)

        if request.names:
            stmt = stmt.filter(self.__tablemodel__.full_name.in_(request.names))

        if request.certification_numbers:
            stmt = stmt.filter(self.__tablemodel__.certification_number.in_(request.certification_numbers))

        return stmt
