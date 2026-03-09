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

import pytest

from nyxera_eye.enrichment.geolocation import geolocate_with_fallback
from nyxera_eye.protocols.onvif_discovery import ONVIFDiscovery
from nyxera_eye.protocols.rtsp_probe import RTSPMetadataProbe
from nyxera_eye.protocols.snmp_metadata import SNMPMetadataExtractor


def test_onvif_discovery_parsing() -> None:
    discovery = ONVIFDiscovery(timeout_seconds=6.0)
    device = discovery.parse_probe_match(
        ip="203.0.113.50",
        xaddr="http://203.0.113.50/onvif/device_service",
        scopes=["onvif://www.onvif.org/type/NetworkVideoTransmitter"],
    )

    assert device.ip == "203.0.113.50"
    assert "onvif" in device.xaddr


def test_rtsp_metadata_probe_parses_public_methods() -> None:
    probe = RTSPMetadataProbe(timeout_seconds=9.0)
    metadata = probe.parse_options_response(
        ip="198.51.100.60",
        port=554,
        response_headers={
            "Server": "RtspServer/1.0",
            "Public": "OPTIONS, DESCRIBE, SETUP, PLAY",
        },
    )

    assert metadata.server == "RtspServer/1.0"
    assert "DESCRIBE" in metadata.methods


def test_snmp_metadata_extractor_safe_mode() -> None:
    extractor = SNMPMetadataExtractor(timeout_seconds=11.0, safe_mode=True)
    metadata = extractor.extract_from_walk(
        ip="192.0.2.10",
        mib_values={
            "1.3.6.1.2.1.1.5.0": "camera-01",
            "1.3.6.1.2.1.1.1.0": "Linux sensor",
            "1.3.6.1.2.1.1.4.0": "secops@example",
        },
    )

    assert metadata.sys_name == "camera-01"


def test_snmp_extractor_rejects_unsafe_mode() -> None:
    extractor = SNMPMetadataExtractor(safe_mode=False)
    with pytest.raises(ValueError, match="unsafe SNMP mode"):
        extractor.extract_from_walk("192.0.2.10", {})


def test_geolocation_fallback_prefers_maxmind() -> None:
    result = geolocate_with_fallback(
        ip="203.0.113.77",
        maxmind_result={"country": "AR", "latitude": -31.4, "longitude": -64.2},
        ipinfo_result={"country": "US", "latitude": 37.7, "longitude": -122.4},
    )

    assert result["country"] == "AR"
    assert result["source"] == "maxmind"
