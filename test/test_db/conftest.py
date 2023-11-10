import pytest
import json

from src.db.session import Base, engine
from settings import MODE

from src.domain import WelderModel, WelderCertificationModel


@pytest.fixture(scope="session", autouse=True)
def prepare_db():
    assert MODE == "TEST"

    Base.metadata.create_all(engine)
    yield
    Base.metadata.drop_all(engine)


@pytest.fixture
def welders() -> list[WelderModel]:
    welders_json = json.load(open("test/test_db/test_welders.json", "r", encoding="utf-8"))

    return [WelderModel.model_validate(welder) for welder in welders_json]
