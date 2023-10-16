from sqlalchemy import select, or_
from sqlalchemy.orm import Session
from sqlalchemy.sql.elements import BinaryExpression

from src.db.db_tables import NDTSummaryTable, WelderCertificationTable, WelderTable
from src.domain import WelderModel, NDTModel
from src.db.engine import engine


kleymos = ["0324", "BEMH"]
names = ["Эрай Мехмет"]
certification_numbers = []

session = Session(engine)

def set_statment(names: list, kleymos: list, certification_numbers: list):
    exps = []
    get_names_expression(names, exps)
    get_kleymo_expression(kleymos, exps)
    get_certification_number_expression(certification_numbers, exps)

    res = session.query(NDTSummaryTable)\
    .join(WelderTable,  WelderTable.kleymo == NDTSummaryTable.kleymo)\
    .join(WelderCertificationTable, NDTSummaryTable.kleymo == WelderCertificationTable.kleymo)\
    .filter(
        or_(*exps)
    )

    return res


def get_kleymo_expression(kleymos: list, exps) -> BinaryExpression | None:
    if len(kleymos) != 0:
        exps.append(NDTSummaryTable.kleymo.in_(kleymos)) 
    
    return None


def get_names_expression(names: list, exps) -> BinaryExpression | None:
    if len(names) != 0:
        exps.append(WelderTable.full_name.in_(names)) 
    
    return None


def get_certification_number_expression(certification_numbers: list, exps) -> BinaryExpression | None:
    if len(certification_numbers) != 0:
        exps.append(WelderCertificationTable.certification_number.in_(certification_numbers)) 
    
    return None


res = set_statment(names, kleymos, certification_numbers)

for el in res:
    print(NDTModel.model_validate(el))
