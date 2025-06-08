import asyncio
import websockets
import sys

current_datetime_message = ""


async def receive_messages(websocket):
    global current_datetime_message
    async for message in websocket:
        if message.startswith("Fibonacci"):
            print(f"\nMensagem do servidor: {message}")
        else:
            current_datetime_message = f"Mensagem do servidor: {message}"
            print(f"\r{current_datetime_message} | Digite um número para calcular Fibonacci ou 'x' para encerrar: ", end="", flush=True)


async def send_messages(websocket):
    loop = asyncio.get_event_loop()
    while True:
        user_input = await loop.run_in_executor(None, input, "   ")
        if user_input.lower() == "x":
            print("\nEncerrando cliente...")
            await websocket.close()
            break
        await websocket.send(user_input)


async def main():
    uri = "ws://localhost:8000/ws"
    async with websockets.connect(uri) as websocket:
        await asyncio.gather(
            receive_messages(websocket),
            send_messages(websocket)
        )

if __name__ == "__main__":
    asyncio.run(main())
