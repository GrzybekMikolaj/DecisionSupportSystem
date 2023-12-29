from typing import Any
from pydantic import AliasChoices, BaseModel, Field


class Data(BaseModel):
    cena: float
    pojemnosc: float
    predkosc_odczytu: float = Field(
        validation_alias=AliasChoices("predkosc-odczytu", "predkosc_odczytu")
    )
    predkosc_zapisu: float = Field(
        validation_alias=AliasChoices("predkosc-zapisu", "predkosc_zapisu")
    )


def parse_weights2dict(data) -> tuple:
    deserialized_data = {}
    alternatives = {}
    algo_settings = []

    for key, value in data.items():
        if key == 'topsis':
            print(value)
            deserialized_data[key] = Data(**dict(value))
            algo_settings = (dict(deserialized_data[key]))
            # print("YOOOOOOOOOOOOOO")
            # print(algo_settings)
            if not algo_settings:
                print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return ["Error"], ["Algor settings incorrect"]
        elif key == 'sp-cs':
            asp_data, ref_data = unpack_spcs_algo_data(value)

            algo_settings.append(asp_data)
            algo_settings.append(ref_data)

            if not algo_settings:
                # print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return ["Error"], ["Algor settings incorrect"]
        # Deserialize alternatives
        else:
            deserialized_data[key] = Data(**dict(value))
            alternatives[key] = (dict(deserialized_data[key]))

    return algo_settings, alternatives


def unpack_spcs_algo_data(data):
    asp_dict = {}
    ref_dict = {}

    for key, value in data.items():
        if key.endswith("-asp"):
            asp_dict[key] = value
        elif key.endswith("-ref"):
            ref_dict[key] = value

    return asp_dict, ref_dict
