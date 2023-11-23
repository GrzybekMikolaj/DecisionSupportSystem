#main.py 
# uvicorn main:app --reload
from fastapi import FastAPI
from core.config import settings
from apis.general_pages.route_homepage import general_pages_router
from fastapi.staticfiles import StaticFiles

def include_router(app):
	app.include_router(general_pages_router)

def start_application():
	app = FastAPI(title=settings.PROJECT_NAME,version=settings.PROJECT_VERSION)
	include_router(app)
	return app 

app = start_application()

@app.post("/algoEnd")
def find_laptop():
    return {"message": "Hello World"} 

app.mount('/', StaticFiles(directory='static'), name='static')
