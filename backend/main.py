from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.requests import Request
from pydantic import BaseModel
import subprocess
import datetime
import report

app = FastAPI()
templates = Jinja2Templates(directory="/frontend/templates")

app = FastAPI()
app.mount("/frontend/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await default_exception_handler(request, exc)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("excepciones.html", {"request": request, "exc": exc}, status_code=500)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_ip = request.client.host
    ct = datetime.datetime.now()
    sheet_id = "1TrUdsIEKcsQnfISTO-XXXUeKHc-1wZNDmMZTZKZ1P78"
    sheet_name = "Hoja1"
    report.generate_ini_google_doc(sheet_id,sheet_name)
    
    context = {
        "request": request,
        "user_ip": user_ip,
        "ct": ct
    }
    return templates.TemplateResponse("index.html", context=context)