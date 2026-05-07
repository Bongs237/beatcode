from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv


def _parse_int(name: str, raw: str | None, *, default: int) -> int:
    if raw is None or raw.strip() == "":
        return default
    try:
        return int(raw.strip())
    except ValueError as e:
        raise ValueError(f"{name} must be an int, got: {raw!r}") from e


def _parse_bool(name: str, raw: str | None, *, default: bool) -> bool:
    if raw is None or raw.strip() == "":
        return default

    v = raw.strip().lower()
    truthy = {"1", "true", "t", "yes", "y", "on"}
    falsy = {"0", "false", "f", "no", "n", "off"}

    if v in truthy:
        return True
    if v in falsy:
        return False
    raise ValueError(f"{name} must be a boolean-like value, got: {raw!r}")


@dataclass(frozen=True)
class Config:
    leetcode_username: str
    min_problems_per_day: int
    processes: list[str]
    poll_interval_seconds: int
    cache_ttl_seconds: int
    fail_open_on_api_error: bool


def load(env_path: str = ".env") -> Config:
    load_dotenv(dotenv_path=env_path, override=False)

    leetcode_username = os.getenv("LEETCODE_USERNAME", "").strip()
    if not leetcode_username:
        raise ValueError("LEETCODE_USERNAME must be set in .env")

    raw_processes = os.getenv("PROCESSES", "").strip()
    if not raw_processes:
        raise ValueError("PROCESSES must be set in .env (comma-separated list)")

    processes = [p.strip() for p in raw_processes.split(",") if p.strip()]
    if not processes:
        raise ValueError("PROCESSES parsed to an empty list; check comma-separated values")

    return Config(
        leetcode_username=leetcode_username,
        min_problems_per_day=_parse_int(
            "MIN_PROBLEMS_PER_DAY", os.getenv("MIN_PROBLEMS_PER_DAY"), default=1
        ),
        processes=processes,
        poll_interval_seconds=_parse_int(
            "POLL_INTERVAL_SECONDS", os.getenv("POLL_INTERVAL_SECONDS"), default=5
        ),
        cache_ttl_seconds=_parse_int(
            "CACHE_TTL_SECONDS", os.getenv("CACHE_TTL_SECONDS"), default=60
        ),
        fail_open_on_api_error=_parse_bool(
            "FAIL_OPEN_ON_API_ERROR", os.getenv("FAIL_OPEN_ON_API_ERROR"), default=True
        ),
    )
