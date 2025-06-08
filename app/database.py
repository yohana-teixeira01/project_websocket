from dotenv import load_dotenv
import os
import redis

load_dotenv()


redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST"),
    port=int(os.getenv("REDIS_PORT")),
    decode_responses=True
)

clients_key = os.getenv("CLIENTS_KEY")

def add_client(client_id):
    redis_client.sadd(clients_key, client_id)
    print(f"Cliente adicionado: {client_id}. Total de clientes: {redis_client.scard(clients_key)}")

def remove_client(client_id):
    redis_client.srem(clients_key, client_id)
    print(f"Cliente removido: {client_id}. Total de clientes: {redis_client.scard(clients_key)}")

def get_all_clients():
    return redis_client.smembers(clients_key)
