from fastapi import WebSocket
from app.database import redis_client, clients_key

class WebSocketConnectionManager:
    def __init__(self):
        self.active_connections: set[WebSocket] = set()

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.add(websocket)
        client_id = str(id(websocket))
        redis_client.sadd(clients_key, client_id)
        print(f"Cliente conectado. Total: {len(self.active_connections)}")

    async def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        client_id = str(id(websocket))
        redis_client.srem(clients_key, client_id)
        print(f"Cliente desconectado. Total: {len(self.active_connections)}")

    async def broadcast(self, message: str):
        disconnected = []
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                disconnected.append(connection)
        for connection in disconnected:
            await self.disconnect(connection)
