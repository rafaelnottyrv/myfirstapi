import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
import functions
from pydantic import BaseModel
import subprocess

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="static/templates")

class FormInput(BaseModel):
    id1: str
    id2: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_ip = request.client.host
    ct = datetime.datetime.now()
    
    context = {
        "request": request,
        "user_ip": user_ip,
        "ct": ct
    }
    return templates.TemplateResponse("index.html", context=context)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await default_exception_handler(request, exc)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("excepciones.html", {"request": request, "exc": exc}, status_code=500)

@app.post("/execute-function")
def execute_function():
    sheet_id = "1TrUdsIEKcsQnfISTO-XXXUeKHc-1wZNDmMZTZKZ1P78"
    sheet_name = "Hoja1"
    functions.generate_ini_google_doc(sheet_id,sheet_name)
    return {"message": "Se ejecutó correctamente el Procesamiento de los Datos"}