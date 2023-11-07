from src.parse_naks.types import WelderData
from src.domain import WelderModel, WelderCertificationModel, Model


class Sorter:

    def sort_welder_data(self, data: list[WelderData]) -> list[WelderModel]:
        data_dict: dict[str, WelderModel] = {}

        for el in data:
            if el.kleymo not in data_dict:
                welder = WelderModel.model_validate(el, from_attributes=True)
                welder.certifications = [WelderCertificationModel.model_validate(el, from_attributes=True)]
                data_dict[el.kleymo] = welder
                continue

            data_dict[el.kleymo].certifications.append(WelderCertificationModel.model_validate(el, from_attributes=True))

        return list(data_dict.values())


    def sort_engineer_data(self, data: list[Model]) -> list[Model]: ...

