from typing import Sequence
from datetime import date

from pydantic import BaseModel
from dateutil import parser

from src.domain.base_domain_model import BaseDomainModel



class DBRequest(BaseModel):
    limit: int = 100
    offset: int = 0


class WelderRequest(DBRequest):
    names: Sequence[str] | None= None
    kleymos: Sequence[str | int] | None = None
    certification_numbers: Sequence[str] | None = None


class WelderCertificationRequest(DBRequest):
    expiration_date_from: date | str | None = None
    expiration_date_before: date | str | None = None


class NDTRequest(DBRequest):
    names: Sequence[str] | None = None
    kleymos: Sequence[str | int] | None = None
    certification_numbers: Sequence[str] | None = None
    comps: Sequence[str] | None = None
    subcomps: Sequence[str] | None = None
    projects: Sequence[str] | None = None
    date_from: date | None = None
    date_before: date | None = None


class DBResponse[Model:BaseDomainModel](BaseModel):
    count: int
    result: Sequence[Model]
