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
from nyxera_eye.workers.pipeline import ProcessingPipeline


def test_processing_pipeline_normalizes_record() -> None:
    record = DeviceRecord(
        source="shodan",
        ip="203.0.113.10",
        port=80,
        protocol="tcp",
        banner="HTTP/1.1 200 OK",
    )

    pipeline = ProcessingPipeline()
    normalized = pipeline.process_record(record)

    assert normalized["service"] == "http"
    assert normalized["risk_profile"] == "medium"
    assert normalized["normalized"] is True
