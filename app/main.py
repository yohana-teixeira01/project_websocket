from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from app.manager import WebSocketConnectionManager  
from datetime import datetime
import asyncio

from app.utils import calculate_fibonacci

app = FastAPI()
manager = WebSocketConnectionManager()

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()  
            n = int(data)  
            fib_result = calculate_fibonacci(n)  
            
            
            await websocket.send_text(f"Fibonacci({n}) = {fib_result}")

    except WebSocketDisconnect:
        await manager.disconnect(websocket)

@app.get("/")
async def root():
    return {"message": "Servidor WebSocket está rodando!"}


async def send_datetime_to_all():
    while True:
        await asyncio.sleep(1) 
        try:
            await manager.broadcast(f"Data e hora atual: {get_current_datetime()}")
        except Exception as e:
            print(f"Erro no broadcast: {e}")

@app.on_event("startup")
async def startup_event():
    asyncio.create_task(send_datetime_to_all())
