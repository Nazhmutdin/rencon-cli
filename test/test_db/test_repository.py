from src.db.repository import NDTRepository
from src.domain import NDTRequest


repository = NDTRepository("ndt_summary_table")

request = NDTRequest(
    names = ['Эрай Мехмет'],
    kleymos = ['0324', 'BEMH'],
    certification_numbers = ['ЮР-14АЦ-I-02133'],
    limit = 100,
    offset = 700
)

print(request)