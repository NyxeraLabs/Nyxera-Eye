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
from nyxera_eye.workers.banner_parser import BannerParsingWorker
from nyxera_eye.workers.device_enrichment import DeviceEnrichmentWorker
from nyxera_eye.workers.service_detection import ServiceDetectionWorker


class ProcessingPipeline:
    def __init__(self) -> None:
        self.banner_worker = BannerParsingWorker()
        self.service_worker = ServiceDetectionWorker()
        self.enrichment_worker = DeviceEnrichmentWorker()

    def process_record(self, record: DeviceRecord) -> dict[str, str | int | None]:
        parsed = self.banner_worker.process(record)
        detected = self.service_worker.process(parsed)
        return self.enrichment_worker.process(detected)

    def process_batch(self, records: list[DeviceRecord]) -> list[dict[str, str | int | None]]:
        return [self.process_record(record) for record in records]
