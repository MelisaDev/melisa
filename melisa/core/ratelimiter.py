# Copyright MelisaDev 2022 - Present
# Full MIT License can be found in `LICENSE.txt` at the project root.

from __future__ import annotations

import logging
from asyncio import sleep
from dataclasses import dataclass
from time import time
from typing import Dict, Tuple, Any

_logger = logging.getLogger("melisa.http")


@dataclass
class RateLimitBucket:
    """Represents a rate limit bucket"""

    limit: int
    remaining: int
    reset: float
    reset_after: float
    since_timestamp: float


class RateLimiter:
    """Prevents ``user`` rate limits"""

    def __init__(self) -> None:
        self.bucket_map: Dict[
            Tuple[str, str], str
        ] = {}  # Dict[Tuple[endpoint, method], bucket_id]
        self.buckets: Dict[str, RateLimitBucket] = {}

    def save_response_bucket(self, endpoint: str, method: str, header: Any):
        ratelimit_bucket_id = header.get("X-RateLimit-Bucket")

        if not ratelimit_bucket_id:
            return

        self.bucket_map[endpoint, method] = ratelimit_bucket_id

        self.buckets[ratelimit_bucket_id] = RateLimitBucket(
            limit=int(header["X-RateLimit-Limit"]),
            remaining=int(header["X-RateLimit-Remaining"]),
            reset=float(header["X-RateLimit-Reset"]),
            reset_after=float(header["X-RateLimit-Reset-After"]),
            since_timestamp=time(),
        )

        _logger.info(
            "Rate limit bucket detected: %s - %r.",
            ratelimit_bucket_id,
            self.buckets[ratelimit_bucket_id],
        )

    async def wait_until_not_ratelimited(self, endpoint: str, method: str):
        bucket_id = self.bucket_map.get((endpoint, method))

        if not bucket_id:
            return

        bucket = self.buckets[bucket_id]

        if bucket.remaining == 0:
            sleep_time = time() - bucket.since_timestamp + bucket.reset_after_timestamp

            _logger.info(
                "Waiting until rate limit for bucket %s is over.", sleep_time, bucket_id
            )

            await sleep(sleep_time)

            _logger.info("Message sent. Bucket %s rate limit ended.", bucket_id)
