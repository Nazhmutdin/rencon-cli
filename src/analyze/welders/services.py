from typing import Sequence, Literal, Protocol, TypeVar
import re

from src.domain import NDTRequest, DBResponse, Name, Kleymo, CertificationNumber
from db.repository import NDTRepository


Saver = TypeVar("Saver", bound="IResultSaveService")


class RequestDataService:
    repository = NDTRepository("ndt_summary_table")
    """
    This Services creates NDTRequest object for NDTRepository
    """
    def _detect_search_key_type(self, search_key: str) -> Literal["name", "kleymo", "certification_number"]:
        if re.fullmatch(r"[\w]+-[\w]+-[I]+-[0-9]+", search_key.strip()):
            return "certification_number"
        
        elif re.fullmatch(r"[A-Z0-9]{4}", search_key.strip()):
            return "kleymo"
        
        return "name"
    
    
    def _sort_search_values(self, search_values: Sequence[Name | Kleymo | CertificationNumber]) -> tuple[Sequence[Name] | None, Sequence[Kleymo] | None, Sequence[CertificationNumber]] | None:
        names = []
        kleymos = []
        certification_numbers = []

        if len(search_values) == 0:
            return (None, None, None)

        for search_value in search_values:

            match self._detect_search_key_type(search_value):
                case "name":
                    names.append(search_value)
                case "kleymo":
                    kleymos.append(search_value)
                case "certification_number":
                    certification_numbers.append(search_value)

        return (names, kleymos, certification_numbers)
        
    
    def _dump_ndt_request(self, **kwargs) -> NDTRequest:
        names, kleymos, certification_numbers = self._sort_search_values(kwargs.get("search_values", []))

        return NDTRequest(
            limit = kwargs.get("limit", None),
            offset = kwargs.get("offset", None),
            names = names,
            kleymos = kleymos,
            certification_numbers = certification_numbers,
            comps = kwargs.get("comps", None),
            subcomps = kwargs.get("subcomps", None),
            projects = kwargs.get("projects", None),
            date_before = kwargs.get("date_before", None),
            date_from = kwargs.get("date_from", None),
        )
    

    def request_data(self, **kwargs) -> DBResponse:
        return self.repository.list(
            self._dump_ndt_request(kwargs=kwargs)
        )


class IResultSaveService(Protocol):

    def save(self) -> None: ...


class ExcelResultSaveService(IResultSaveService):

    def save(self) -> None: ...


class PDFResultSaveService(IResultSaveService):

    def save(self) -> None: ...
