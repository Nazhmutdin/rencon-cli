from typing import TypeAlias, TypeVar, Union, Sequence
from dataclasses import dataclass

from pydantic import BaseModel


"""
=======================================================================================================
Types
=======================================================================================================
"""


Limit: TypeAlias = int
Offset: TypeAlias = int
Name: TypeAlias = str
Kleymo: TypeAlias = str
CertificationNumber: TypeAlias = str
Company: TypeAlias = str
SubCompany: TypeAlias = str
Project: TypeAlias = str
DateFrom: TypeAlias = str
DateBefore: TypeAlias = str
Count: TypeAlias = int
Model = TypeVar("Model", bound=BaseModel)


"""
=======================================================================================================
value objects
=======================================================================================================
"""


@dataclass
class DBRequest:
    limit: Limit
    offset: Offset


@dataclass
class WelderRequest(DBRequest):
    names: Sequence[Name]
    kleymos: Sequence[Kleymo]
    certification_numbers: Sequence[CertificationNumber]


class NDTRequest(DBRequest):
    names: Sequence[Name]
    kleymos: Sequence[Kleymo]
    certification_numbers: Sequence[CertificationNumber]
    comps: Sequence[Company]
    subcomps: Sequence[SubCompany]
    projects: Sequence[Project]
    date_from: DateFrom
    date_before: DateBefore


@dataclass
class DBResponse:
    count: Count
    summary_count: Count
    result: Sequence[Model]
