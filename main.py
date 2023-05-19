from fastapi import FastAPI, Request, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
app = FastAPI()
templates = Jinja2Templates(directory="templates")

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    if exc.status_code == 404:
        return templates.TemplateResponse("404.html", {"request": request}, status_code=404)
    return exc

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    user_ip = request.client.host
    context = {
        "request": request,
        "user_ip": user_ip
    }
    return templates.TemplateResponse("index.html", context=context)