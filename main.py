from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse,StreamingResponse,JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dependency.Camera import video
from dependency.Dobot import position
import uvicorn

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/VIDFeed")
async def VIDFeed():
    return StreamingResponse(video(), media_type="multipart/x-mixed-replace; boundary=frame")

@app.get("/BotPosition")
async def Location():
    position_data = position()    
    
    if position_data is None:
      return JSONResponse(content={"error": "Library hasn't been initialized yet."}, status_code=400)
    
    x, y, z, r, j1, j2, j3, j4 = position_data
    return JSONResponse(content={
        "x": x,
        "y": y,
        "z": z,
        "r": r,
        "j1": j1,
        "j2": j2,
        "j3": j3,
        "j4": j4
    })
    

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")