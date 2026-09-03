import os
from dataclasses import dataclass
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


def _parse_bool(value: str) -> bool:
    return value.strip().lower() in {"1", "true", "yes", "y", "on"}


@dataclass
class Settings:
    bot_token: str
    gemini_api_key: str
    webhook_base: str = "http://localhost:8080"
    webhook_path: str = "/webhook"
    webhook_secret: Optional[str] = None
    web_server_host: str = "0.0.0.0"
    web_server_port: int = 8080
    gemini_model: str = "gemini-2.5-flash"
    use_webhook: bool = True

    @property
    def webhook_url(self) -> str:
        return f"{self.webhook_base.rstrip('/')}{self.webhook_path}"

    @classmethod
    def from_env(cls) -> "Settings":
        bot_token = os.getenv("BOT_TOKEN")
        gemini_api_key = os.getenv("GEMINI_API_KEY")

        if not bot_token:
            raise RuntimeError("Missing required environment variable: BOT_TOKEN")
        if not gemini_api_key:
            raise RuntimeError("Missing required environment variable: GEMINI_API_KEY")

        webhook_base = os.getenv("WEBHOOK_BASE", cls.webhook_base)
        webhook_path = os.getenv("WEBHOOK_PATH", cls.webhook_path)
        webhook_secret = os.getenv("WEBHOOK_SECRET")
        web_server_host = os.getenv("WEB_SERVER_HOST", cls.web_server_host)
        web_server_port = int(os.getenv("WEB_SERVER_PORT", cls.web_server_port))
        gemini_model = os.getenv("GEMINI_MODEL", cls.gemini_model)
        use_webhook = _parse_bool(os.getenv("USE_WEBHOOK", "true"))

        return cls(
            bot_token=bot_token,
            gemini_api_key=gemini_api_key,
            webhook_base=webhook_base,
            webhook_path=webhook_path,
            webhook_secret=webhook_secret,
            web_server_host=web_server_host,
            web_server_port=web_server_port,
            gemini_model=gemini_model,
            use_webhook=use_webhook,
        )
