import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_path: str = os.getenv("HF_MODEL", "DavitIshkhanyan/best-ner-model")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    # HOST: str = os.getenv("HOST", "127.0.0.1")
    # PORT: int = int(os.getenv("PORT", "8000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")
    PORT: int = int(os.getenv("PORT", "8000"))
    # bot_mode: str = "polling"
    # webhook_url: str = "https://example.com/bot/webhook/change_me"
    # webhook_secret: str = "change_me"
    # start_poller: bool = False

    class Config:
        env_file = ".env"

    @property
    def api_url(self) -> str:
        return f"http://{self.HOST}:{self.PORT}/predict"

settings = Settings()
