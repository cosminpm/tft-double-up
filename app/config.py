from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    tft_url: str = "https://tftactics.gg"
    tft_champion_url: str = "https://raw.communitydragon.org"
    is_sentry: bool = True
    host: str = "0.0.0.0"
    port: int = 8080

    debug: bool = False
