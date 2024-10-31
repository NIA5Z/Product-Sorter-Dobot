from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,StreamingResponse,JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dependency.Dobot import init,position,move,home,partol,close
from dependency.Camera import video
from pydobot import Dobot
from functools import cache 
import httpx 
import uvicorn

app = FastAPI() 
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
start,status = False,None

origins = [
    "http://localhost:8000",
    "http://localhost:1433"
]

SQLServer=str(input("Give me the IP for SQL Server API: "))
origins.append(SQLServer)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

@cache
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    global SQLServer
    try:
     async with httpx.AsyncClient() as client:
        response = await client.get(SQLServer)
        return templates.TemplateResponse("client.html", {"request": request, "data": response.json()})
    except:
       print("Warning: The SQL Server is not up, switching to Local Mode.")
       return templates.TemplateResponse("client.html", {"request": request})

@app.get("/VIDFeed")
async def VIDFeed():
    global start,status,SQLServer
    if start:
     status="Checked"
     device = Dobot(port="COM3")
     init(device)
     return StreamingResponse(video(Source=0,web=SQLServer), media_type="multipart/x-mixed-replace; boundary=frame")
    return

@app.get("/start")
async def Start():
    global start,status
    start = True
    if status is None:
     await VIDFeed()
    else:
       return {"start": "The process is running."}

@app.get("/close")
async def close_device():
    global start
    start=False
    close()
    return 

@app.get("/home")   
async def home_device(overwrite: bool = False, recall: bool = False):
    home(recall=recall)
    return 

@app.get("/position")
async def get_position():
    pos = position()
    return {"position": pos}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")