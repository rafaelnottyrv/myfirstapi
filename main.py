import datetime
from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
from starlette.requests import Request
from fastapi.templating import Jinja2Templates
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import functions
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

@app.post("/procesar")
def procesar(id1: str = Form(...), id2: str = Form(...)):
    functions.generate_ini_google_doc(id1,id2)
    return {"message": "Se ejecutó correctamente el Procesamiento de los Datos"}

@app.post("/resultados")
def resultados():
        return HTMLResponse("""
        <html>
        <head>
            <title>Redirección</title>
            <script>
                window.open("https://docs.google.com/", "_blank");
            </script>
        </head>
        <body>
            <h1>Redirigiendo...</h1>
            <h3>Dale clic a permitir ventanas emergentes</h3>
        </body>
        </html>
    """)