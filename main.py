#main.py 
# uvicorn main:app --reload
from fastapi import FastAPI
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from fastapi.staticfiles import StaticFiles
from topsis import topsis
from file_handler import read_json, write_json
from pydantic import BaseModel, Field

class Weights(BaseModel):
    marka: int 
    cena: int
    pojemnosc: int
    predkosc_odczytu: int = Field(
		alias = "predkosc-odczytu"
	)
    predkosc_zapisu: int = Field(
		alias = "predkosc-zapisu"
	)


class Data(BaseModel):
    marka: str 
    cena: int
    pojemnosc: int
    predkosc_odczytu: int = Field(
		alias = "predkosc-odczytu"
	)
    predkosc_zapisu: int = Field(
		alias = "predkosc-zapisu"
	)



def include_router(app):
	app.include_router(general_pages_router)

def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	return app 

app = start_application()

@app.post("/api/endpoint")
def find_laptop(data: dict[str, Data | Weights]):
	# print(data)
	result = topsis(data) 
	print(result)
	# if result is not None:
	# 	output = write_json('results.json', {"Rankings": result})
	# 	return output
	return data 

app.mount('/', StaticFiles(directory='static'), name='static')
