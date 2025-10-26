# src/config.py
from dataclasses import dataclass
from typing import List, Dict
import os
from dotenv import load_dotenv


# Allow choosing environment file via ENV_FILE variable
env_file = os.getenv("ENV_FILE", ".env")
load_dotenv(env_file)


@dataclass
class Config:
    """Holds application configuration loaded from environment variables."""
    api_id: int
    api_hash: str
    make_webhook_url: str
    channels: List[str]
    keywords: Dict[str, List[str]]
    check_interval_hours: int


def load_config() -> Config:
    """
    Load environment variables and return a Config object.
    Supports multiple keyword groups with KEYWORDS_* variables.
    """
    api_id = int(os.getenv("API_ID", "0"))
    api_hash = os.getenv("API_HASH", "")
    make_webhook_url = os.getenv("MAKE_WEBHOOK_URL", "")

    # Parse channel list
    channels = [
        c.strip() for c in os.getenv("CHANNELS", "").split(",") if c.strip()
    ]

    # Parse keyword groups (e.g. KEYWORDS_NEWS, KEYWORDS_BIKE)
    keywords: Dict[str, List[str]] = {}
    for key, value in os.environ.items():
        if key.startswith("KEYWORDS_"):
            group_name = key.replace("KEYWORDS_", "").lower()
            keywords[group_name] = [
                v.strip() for v in value.split(",") if v.strip()
            ]

    check_interval_hours = int(os.getenv("CHECK_INTERVAL_HOURS", "8"))

    return Config(
        api_id=api_id,
        api_hash=api_hash,
        make_webhook_url=make_webhook_url,
        channels=channels,
        keywords=keywords,
        check_interval_hours=check_interval_hours,
    )
