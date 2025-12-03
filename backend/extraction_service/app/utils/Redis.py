import redis
import os
import dotenv

REDIS_HOST = os.getenv("REDIS_HOST_ADDRESS")
REDIS_PORT = os.getenv("REDIS_PORT_NUMBER")

pool = redis.ConnectionPool(REDIS_HOST,REDIS_PORT, db=0)
r = redis.Redis(connection_pool=pool, decode_responses=True)