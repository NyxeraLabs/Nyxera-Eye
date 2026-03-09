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

from internal.intel.fingerprint.device_fingerprint import (
    build_web_fingerprint,
    detect_device_model_hint,
    detect_firmware_version_hint,
    parse_html_title_and_metadata,
    parse_http_server_header,
)

__all__ = [
    "build_web_fingerprint",
    "detect_device_model_hint",
    "detect_firmware_version_hint",
    "parse_html_title_and_metadata",
    "parse_http_server_header",
]
