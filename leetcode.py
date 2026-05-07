from __future__ import annotations

import sys
import time
from datetime import date, datetime
from typing import Any

import requests

from config import Config

GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query recent($username: String!, $limit: Int!) {
  recentAcSubmissionList(username: $username, limit: $limit) {
    titleSlug
    timestamp
  }
}
"""


class LeetCodeClient:
    def __init__(self, cfg: Config) -> None:
        self._cfg = cfg
        self._cache_value: int | None = None
        self._cache_expires: float = 0.0
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Content-Type": "application/json",
                "User-Agent": "GoofyAhhGate/1.0 (personal monitoring; +https://leetcode.com)",
                "Referer": "https://leetcode.com/",
            }
        )

    def invalidate(self) -> None:
        self._cache_value = None
        self._cache_expires = 0.0

    def solved_today_count(self) -> int | None:
        now = time.monotonic()
        if self._cache_value is not None and now < self._cache_expires:
            return self._cache_value

        count = self._fetch_solved_today()
        if count is None:
            # Do not serve stale counts after a failed refresh.
            self.invalidate()
            return None

        self._cache_value = count
        self._cache_expires = now + self._cfg.cache_ttl_seconds
        return count

    def _fetch_solved_today(self) -> int | None:
        payload: dict[str, Any] = {
            "query": QUERY,
            "variables": {"username": self._cfg.leetcode_username, "limit": 20},
        }
        try:
            r = self._session.post(GRAPHQL_URL, json=payload, timeout=15)
            r.raise_for_status()
            data = r.json()
        except Exception as e:
            print(f"[leetcode] request failed: {e}", file=sys.stderr)
            return None

        if data.get("errors"):
            print(f"[leetcode] graphql errors: {data['errors']}", file=sys.stderr)
            return None

        try:
            submissions = data["data"]["recentAcSubmissionList"] or []
        except (KeyError, TypeError) as e:
            print(f"[leetcode] unexpected response shape: {e}", file=sys.stderr)
            return None

        today = date.today()
        seen: set[str] = set()
        for sub in submissions:
            if not sub:
                continue
            slug = sub.get("titleSlug")
            ts_raw = sub.get("timestamp")
            if not slug or ts_raw is None:
                continue
            try:
                ts = int(ts_raw)
            except (TypeError, ValueError):
                continue
            submitted = datetime.fromtimestamp(ts).date()
            if submitted == today:
                seen.add(str(slug))

        return len(seen)
