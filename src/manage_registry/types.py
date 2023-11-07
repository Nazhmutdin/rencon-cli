from pydantic import BaseModel


class InvoiceRow(BaseModel):
    service_name: str
    amount: int
    price: int | float
    methods: list[str] | None = None
    names: list[str] | None = None


class WelderListRow(BaseModel):
    full_name_rus: str
    full_name: str
    project: str
    subcomp: str
    method: str
