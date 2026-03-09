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

from nyxera_eye.fingerprinting import (
    build_web_fingerprint,
    detect_device_model_hint,
    detect_firmware_version_hint,
    parse_html_title_and_metadata,
    parse_http_server_header,
)


def test_parse_http_server_header_normalizes_spacing() -> None:
    assert parse_http_server_header("  nginx/1.25.3   ") == "nginx/1.25.3"


def test_parse_html_title_and_metadata_extracts_title_and_meta() -> None:
    title, metadata = parse_html_title_and_metadata(
        """
        <html>
          <head>
            <title>Axis P3225-LV</title>
            <meta name="generator" content="Firmware 10.12.3">
            <meta property="og:site_name" content="Axis Camera Portal">
          </head>
        </html>
        """
    )

    assert title == "Axis P3225-LV"
    assert metadata["generator"] == "Firmware 10.12.3"
    assert metadata["og:site_name"] == "Axis Camera Portal"


def test_detect_device_model_hint_matches_known_patterns() -> None:
    model = detect_device_model_hint("Edge camera :: Axis P3225-LV network camera")

    assert model == "Axis P3225-LV"


def test_detect_firmware_version_hint_matches_common_formats() -> None:
    version = detect_firmware_version_hint("generator=Firmware version 10.12.3")

    assert version == "10.12.3"


def test_build_web_fingerprint_combines_all_web_signals() -> None:
    fingerprint = build_web_fingerprint(
        server_header="Boa/0.94.14rc21",
        html="""
        <html>
          <head>
            <title>Moxa NPort 5110A</title>
            <meta name="generator" content="Firmware 3.11">
          </head>
        </html>
        """,
        favicon_bytes=b"nyxera-favicon",
    )

    assert fingerprint["http_server"] == "Boa/0.94.14rc21"
    assert fingerprint["html_title"] == "Moxa NPort 5110A"
    assert fingerprint["favicon_hash"] is not None
    assert fingerprint["model_hint"] == "Moxa NPort 5110A"
    assert fingerprint["firmware_hint"] == "3.11"
