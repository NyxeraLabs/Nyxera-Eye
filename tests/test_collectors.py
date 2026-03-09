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

from nyxera_eye.collectors.censys import CensysCollector
from nyxera_eye.collectors.dork_manager import DorkManager
from nyxera_eye.collectors.shodan import ShodanCollector
from nyxera_eye.collectors.zoomeye import ZoomEyeCollector
from tests.mocks.osint_payloads import CENSYS_PAYLOAD, SHODAN_PAYLOAD, ZOOMEYE_PAYLOAD


def test_shodan_collector_normalization() -> None:
    collector = ShodanCollector(api_key="demo")
    records = collector.normalize_payload(SHODAN_PAYLOAD)

    assert len(records) == 1
    assert records[0].source == "shodan"
    assert records[0].ip == "198.51.100.10"
    assert records[0].port == 80


def test_censys_collector_normalization() -> None:
    collector = CensysCollector(api_key="demo")
    records = collector.normalize_payload(CENSYS_PAYLOAD)

    assert len(records) == 1
    assert records[0].source == "censys"
    assert records[0].ip == "203.0.113.44"
    assert records[0].port == 443


def test_zoomeye_collector_normalization() -> None:
    collector = ZoomEyeCollector(api_key="demo")
    records = collector.normalize_payload(ZOOMEYE_PAYLOAD)

    assert len(records) == 1
    assert records[0].source == "zoomeye"
    assert records[0].ip == "192.0.2.77"
    assert records[0].port == 502


def test_dork_manager_rotation_and_rate_limit() -> None:
    manager = DorkManager(
        categories={"ics": ["port:502", "port:20000"]},
        rate_limit_seconds={"ics": 2.0},
    )

    assert manager.next_query("ics", now=10.0) == "port:502"
    assert manager.next_query("ics", now=11.0) is None
    assert manager.next_query("ics", now=12.1) == "port:20000"
    assert manager.next_query("ics", now=14.3) == "port:502"
