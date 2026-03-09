# Copyright (c) 2026 NyxeraLabs
# Author: José María Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 → Apache-2.0
#
# You may:
# ✔ Study
# ✔ Modify
# ✔ Use for internal security testing
#
# You may NOT:
# ✘ Offer as a commercial service
# ✘ Sell derived competing products

try:
    from arq import create_pool
    from arq.connections import RedisSettings
except ImportError:  # pragma: no cover
    create_pool = None
    RedisSettings = None


class RedisTaskQueue:
    def __init__(self, host: str = "127.0.0.1", port: int = 6379, database: int = 0) -> None:
        self.host = host
        self.port = port
        self.database = database

    async def enqueue_osint_task(self, provider: str, query: str, page: int = 1) -> None:
        if create_pool is None or RedisSettings is None:
            raise RuntimeError("arq dependency is required for Redis queue integration")

        redis = await create_pool(
            RedisSettings(
                host=self.host,
                port=self.port,
                database=self.database,
            )
        )
        await redis.enqueue_job(
            "process_osint_query",
            {
                "provider": provider,
                "query": query,
                "page": page,
            },
        )
        await redis.close()
