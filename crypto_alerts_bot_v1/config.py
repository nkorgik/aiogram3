from dataclasses import dataclass
import os


def _env_int(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None:
        return default
    try:
        return int(value)
    except ValueError:
        return default


def _env_bool(name: str, default: bool) -> bool:
    value = os.getenv(name)
    if value is None:
        return default
    return value.strip().lower() not in {"0", "false", "no", "off"}


@dataclass
class BotConfig:
    db_name: str
    quote_asset: str
    check_interval_seconds: int
    max_alerts_per_user: int
    show_console_status: bool


config = BotConfig(
    db_name=os.getenv("CRYPTO_WATCHMAN_DB", "crypto_watchman.db"),
    quote_asset=os.getenv("CRYPTO_WATCHMAN_QUOTE", "USDT"),
    check_interval_seconds=_env_int("CRYPTO_WATCHMAN_INTERVAL", 60),
    max_alerts_per_user=_env_int("CRYPTO_WATCHMAN_MAX_ALERTS_PER_USER", 20),
    show_console_status=_env_bool("CRYPTO_WATCHMAN_CONSOLE_STATUS", True),
)

