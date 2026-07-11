import os

import httpx
import pytest
from dotenv import load_dotenv, find_dotenv

from src.config.base import BaseConfig


@pytest.fixture(scope="session")
def session():
    limits = httpx.Limits(max_keepalive_connections=5, max_connections=20)
    timeout = httpx.Timeout(timeout=10.0)

    with httpx.Client(limits=limits, timeout=timeout) as client:
        yield client


@pytest.fixture(scope="session")
def base_config():
    env_path = find_dotenv(".env.local")
    if not env_path:
        raise FileNotFoundError(
            "Could not locate your '.env.local' configuration file in the workspace root."
        )

    load_dotenv(dotenv_path=env_path)

    base_url = os.getenv("BASE_URL")
    if not base_url:
        raise ValueError(
            "The 'BASE_URL' environment variable is missing or empty inside your .env.local file."
        )

    clean_url = base_url.rstrip("/")

    return BaseConfig(base_url=clean_url)


@pytest.fixture(scope="function")
def base_headers() -> dict[str, str]:
    return {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "User-Agent": "Automation-Python-Hybrid/1.0 (HTTPX Client)",
    }
