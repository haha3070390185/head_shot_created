import os
from dotenv import load_dotenv
from functools import lru_cache

load_dotenv()


class Settings:
    def __init__(self):
        self.dashscope_api_key = os.getenv("DASHSCOPE_API_KEY", "")


@lru_cache()
def get_settings():
    return Settings()
