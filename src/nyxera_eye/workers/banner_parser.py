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

from nyxera_eye.collectors.models import DeviceRecord


class BannerParsingWorker:
    def process(self, record: DeviceRecord) -> dict[str, str | int | None]:
        return {
            "ip": record.ip,
            "port": record.port,
            "protocol": record.protocol,
            "banner": (record.banner or "").strip() or None,
            "source": record.source,
        }
