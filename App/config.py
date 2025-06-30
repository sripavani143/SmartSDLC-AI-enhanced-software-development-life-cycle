import os
from dotenv import load_dotenv

load_dotenv()

WATSONX_API_KEY = os.getenv("WATSONX_API_KEY")
WATSONX_PROJECT_ID = os.getenv("WATSONX_PROJECT_ID")
WATSONX_MODEL_ID = os.getenv("WATSONX_MODEL_ID")
WATSONX_URL = os.getenv("WATSONX_URL")

# ✅ Debug line to check
print("✅ Loaded model from .env:", WATSONX_MODEL_ID)
