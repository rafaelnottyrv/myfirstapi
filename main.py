import datetime
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
import report
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
    sheet_id = "1TrUdsIEKcsQnfISTO-XXXUeKHc-1wZNDmMZTZKZ1P78"
    sheet_name = "Hoja1"
    report.generate_ini_google_doc(sheet_id,sheet_name)
    
    context = {
        "request": request,
        "user_ip": user_ip,
        "ct": ct
    }
    return templates.TemplateResponse("index.html", context=context)

@app.post("/process")
async def process(form_input: FormInput):
    result = subprocess.run(["python", "function1.py", form_input.id1, form_input.id2], capture_output=True)
    if result.returncode == 0:
        return {"message": result.stdout.decode()}
    else:
        return {"message":"Hola"}

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return await default_exception_handler(request, exc)

@app.exception_handler(Exception)
async def default_exception_handler(request: Request, exc: Exception):
    return templates.TemplateResponse("excepciones.html", {"request": request, "exc": exc}, status_code=500)

@app.post("/api/function1")
async def process_form_data(data: dict):
    id1 = data.get("id1")
    id2 = data.get("id2")

    # Ejecutar el código desde function1.py
    result = function1.execute(id1, id2)

    # Hacer algo con el resultado (por ejemplo, devolverlo como respuesta JSON)
    return {"result": result}