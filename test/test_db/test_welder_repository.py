import pytest

from src.db.repository import WelderRepository
from src.domain import WelderModel


class TestWelderRepository:
    repo = WelderRepository()


    @pytest.mark.usefixtures('welders')
    def test_add(self, welders) -> None: 
        self.repo.add(welders)
        assert self.repo.count == len(welders)


    @pytest.mark.parametrize(
            "id, expectation",
            [
                ("7H47", WelderModel),
                ("9EBT", WelderModel),
                ("7CE3", WelderModel),
            ]
    )
    def test_get_1(self, id: int | str, expectation: WelderModel | None) -> None:
        assert type(self.repo.get(id)) == expectation


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 3, 4, 5, 6]
    )
    def test_get_2(self, index: int, welders: list[WelderModel]) -> None:
        welder = welders[index]
        assert self.repo.get(welder.kleymo) == welder


    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 2, 63, 4, 5, 11]
    )
    def test_add_with_existing_welder(self, welders: list[WelderModel], index: int) -> None:
        self.repo.add([welders[index]])

        assert self.repo.count == len(welders)

    
    @pytest.mark.usefixtures('welders')
    @pytest.mark.parametrize(
            "index",
            [1, 42, 76, 4, 33, 15]
    )
    def test_update(self, welders: list[WelderModel], index: int) -> None:
        welder = welders[index]
        welder.full_name = f"Name_{index}"

        self.repo.update([welder])
        updated_welder = self.repo.get(welder.kleymo)
        assert updated_welder.full_name == welder.full_name

    
    @pytest.mark.usefixtures('welders')
    def test_delete(self, welders: list[WelderModel]) -> None:
        welder = welders[0]

        self.repo.delete([welder])
        assert self.repo.count == len(welders) - 1