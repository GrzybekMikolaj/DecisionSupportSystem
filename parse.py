from typing import Any
from pydantic import AliasChoices, BaseModel, Field

# class Weights(BaseModel):
#     cena: int
#     pojemnosc: int
#     predkosc_odczytu: int = Field(
# 		alias = "predkosc-odczytu"
# 	)
#     predkosc_zapisu: int = Field(
# 		alias = "predkosc-zapisu"
# 	)

class Data(BaseModel):
    cena: int
    pojemnosc: int
    predkosc_odczytu: int = Field(
		validation_alias = AliasChoices("predkosc-odczytu", "predkosc_odczytu")
	)
    predkosc_zapisu: int = Field(
		validation_alias = AliasChoices("predkosc-zapisu", "predkosc_zapisu")
	)


def parse_weights2dict(data) -> dict:
    deserialized_data = {}
    alternatives = {}
    algo_settings = []

    for key, value in data.items():
        if key == 'topsis':
            deserialized_data[key] = Data(**dict(value))
            algo_settings = (dict(deserialized_data[key]))
            # print("YOOOOOOOOOOOOOO")
            # print(algo_settings)
            if not algo_settings:
                print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return{"Error": "0"}
        elif key == 'sp-cs':
            deserialized_data[key] = Data(**value)
            # print(deserialized_data[key])
            algo_settings = deserialized_data[key]
            if not algo_settings:
                # print("Brak prawidłowych wag. Algorytm nie może być wykonany.")
                return{"Error": "0"}
        # Deserialize alternatives
        else: 
            deserialized_data[key] = Data(**dict(value))
            alternatives[key] = (dict(deserialized_data[key]))
    
    return(algo_settings, alternatives)
