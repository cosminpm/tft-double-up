from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    tft_url: str = "http://127.0.0.2:9999/fake-tft"
