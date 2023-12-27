#main.py 
# uvicorn main:app --reload
from fastapi import FastAPI
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from fastapi.staticfiles import StaticFiles
from topsis import topsisMethod
from file_handler import read_json, write_json
from parse import Data

def include_router(app):
	app.include_router(general_pages_router)

def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	return app 

app = start_application()

@app.post("/api/endpoint")
def find_laptop(data: dict[str, Data]):
	result = topsisMethod(data)
	return result

app.mount('/', StaticFiles(directory='static'), name='static')
