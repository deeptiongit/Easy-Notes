from fastapi import FastAPI, Request, BackgroundTasks
import redis, pickle, json, logging, os
import requests
import numpy as np

# --- Configuration ---
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))
AGENT1_URL = os.getenv("AGENT1_URL", "http://agent1:8001/training")

# --- Redis & Logging ---
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=False)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Agent2-Integration")

# --- App Setup ---
app = FastAPI()
model_key = "agent2:model"
data_key = "agent2:failure_logs"
feedback_key = "agent2:human_feedback"

