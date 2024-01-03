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
            # TODO: rework to use upack_algo_data()
            print(value)
            deserialized_data[key] = Data(**dict(value))
            algo_settings = (dict(deserialized_data[key]))
            # print("YOOOOOOOOOOOOOO")
            # print(algo_settings)
            if not algo_settings:
                print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return ["Error"], ["Algor settings incorrect"]
        elif key == 'sp-cs':
            asp_data, status_quo_data, opt_lim_data = unpack_algo_data(value)

            algo_settings.append(asp_data)
            algo_settings.append(status_quo_data)

            if not algo_settings:
                # print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return ["Error"], ["Algor settings incorrect"]
        elif key == 'rms':
            asp_data, status_quo_data, opt_lim_data = unpack_algo_data(value)

            algo_settings.append(asp_data)
            algo_settings.append(status_quo_data)
            algo_settings.append(opt_lim_data)

            if not algo_settings:
                # print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return ["Error"], ["Algor settings incorrect"]
        # Deserialize alternatives
        else:
            deserialized_data[key] = Data(**dict(value))
            alternatives[key] = (dict(deserialized_data[key]))

    return algo_settings, alternatives


def unpack_algo_data(data):
    asp_dict = {}
    status_quo_dict = {}
    opt_lim_dict = {}  # dictionary of opoptimality limitfor the solution

    for key, value in data.items():
        if key.endswith("-asp"):
            asp_dict[key] = value
        elif key.endswith("-ref"):
            status_quo_dict[key] = value
        elif key.endswith("-gran"):
            opt_lim_dict[key] = value

    return asp_dict, status_quo_dict, opt_lim_dict
