"""Configuration loader. Reads .env from repo root."""
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import os

PROJECT_ROOT = Path(__file__).resolve().parent


@dataclass(frozen=True)
class Config:
    openai_api_key: str


def load_config() -> Config:
    load_dotenv(PROJECT_ROOT / ".env", override=True)
    return Config(
        openai_api_key=os.environ.get("OPENAI_API_KEY", ""),
    )
