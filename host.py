from fastapi import FastAPI, Request,Query,WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse,StreamingResponse,JSONResponse, RedirectResponse 
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from functools import cache 
from dependency.SQLData import create_table,fetchall,update,insert,fetch,remove
from pydantic import BaseModel
import uvicorn
import asyncio

origins = [
    "http://localhost:8000", 
]

app= FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
create_table(overwrite=True)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],  
)

class SQLData_Input(BaseModel):
    CODE: int
    BRAND:str
    NAME: str
    TYPE: str
    PUnit: float
    PBase: int
    QTY: int

active_connections = []

@cache
@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    Fetchdata = fetchall()
    return templates.TemplateResponse("host.html", {"request": request, "data": Fetchdata})

@app.get("/data", response_class=JSONResponse)
async def fetchALL_data():
    Fetchdata = fetchall()
    await notify_clients()
    return Fetchdata

@app.get("/fetch")
async def fetch_data(CODE: int = Query(...)):
    single_data = fetch(CODE)
    return single_data

@app.get("/update")
async def update_data(CODE: int = Query(...),BRAND: str = Query(...),NAME: str = Query(...),TYPE: str = Query(...),PUnit: float = Query(...),PBase: int = Query(...),QTY: int = Query(...)):
    sql_data = ModelInsert(CODE,BRAND,NAME,TYPE,PUnit,PBase,QTY)
    update(sql_data)
    await notify_clients()
    return RedirectResponse(url="/", status_code=303)

@app.get("/insert")
async def insert_data(CODE: int = Query(...),BRAND: str = Query(...),NAME: str = Query(...),TYPE: str = Query(...),PUnit: float = Query(...),PBase: int = Query(...),QTY: int = Query(...)):
    sql_data = ModelInsert(CODE,BRAND,NAME,TYPE,PUnit,PBase,QTY)
    insert(sql_data)
    await notify_clients()
    return RedirectResponse(url="/", status_code=303)

@app.get("/remove")
async def remove_data(target,CODE):
    remove(target,CODE)
    await notify_clients()
    return RedirectResponse(url="/", status_code=303)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_connections.append(websocket)
    try:
        while True:
            await websocket.receive_text()  
    except WebSocketDisconnect:
        active_connections.remove(websocket)

def ModelInsert(CODE,BRAND,NAME,TYPE,PUnit,PBase,QTY):
    sql_data = SQLData_Input(
        CODE=CODE,
        BRAND=BRAND,
        NAME=NAME,
        TYPE=TYPE,
        PUnit=PUnit,
        PBase=PBase,
        QTY=QTY
    )
    return sql_data

async def notify_clients():
    message = "Data updated"
    for connection in active_connections:
        await connection.send_text(message)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=1433, log_level="info")

#http://127.0.0.1:8000/insert?CODE=532&BRAND=ExampleBrand&NAME=ExampleName&TYPE=ExampleType&PUnit=10.99&PBase=100&QTY=50
#[1,53335521,"Sony","Playstation 5","Eletronic",499.99,399,1]
#http://127.0.0.1:8000/update?CODE=53335521&BRAND=Brony&NAME=Ponestation 420&TYPE=Electronic&PUnit=500&PBase=399&QTY=0