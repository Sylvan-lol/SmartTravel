import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ZHIPU_API_KEY = os.getenv("ZHIPU_API_KEY")
    HEFENG_API_KEY = os.getenv("HEFENG_API_KEY")
    AMAP_API_KEY = os.getenv("AMAP_API_KEY")
    LLM_API_KEY = os.getenv("LLM_API_KEY")
    LLM_BASE_URL = os.getenv("LLM_BASE_URL")
    LLM_MODEL = os.getenv("LLM_MODEL")