from src.domain import WelderModel, WelderCertificationModel
from src.parse_naks.types import WelderData


class WelderCertificationSorter:
    def _certifications_list_to_model(self, certifications: list[WelderData]) -> WelderCertificationModel:
        return [WelderCertificationModel.model_validate(certification) for certification in certifications]


    def _welder_dict_to_model(self, welder: dict) -> WelderModel:
        return WelderModel(
            kleymo=welder["kleymo"],
            full_name=welder["full_name"],
            certifications=self._certifications_list_to_model(welder["certifications"])
        )


    def sort_certifications(self, data: list[WelderData]) -> list[WelderModel]:
        welders: dict[str, dict[str, str | list]] = {}
        for welder_row in data:
            if welder_row.kleymo not in welders:
                welders[welder_row.kleymo] = {
                    "full_name": welder_row.full_name,
                    "kleymo": welder_row.kleymo,
                    "certifications": [welder_row]
                }

                continue
            
            welders[welder_row.kleymo]["certifications"].append(welder_row)


        return [self._welder_dict_to_model(welder) for welder in welders.values() if welder["kleymo"] != None]
