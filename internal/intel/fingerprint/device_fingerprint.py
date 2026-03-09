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

from __future__ import annotations

import re
from html.parser import HTMLParser

from nyxera_eye.fingerprinting.murmurhash3 import favicon_mmh3_from_bytes


_MODEL_PATTERNS = [
    re.compile(r"\b(axis\s+[a-z0-9-]+(?:\s+[a-z0-9-]+){0,2})\b", re.IGNORECASE),
    re.compile(r"\b(hikvision\s+[a-z0-9-]+(?:\s+[a-z0-9-]+){0,2})\b", re.IGNORECASE),
    re.compile(r"\b(dahua\s+[a-z0-9-]+(?:\s+[a-z0-9-]+){0,2})\b", re.IGNORECASE),
    re.compile(r"\b(moxa\s+[a-z0-9-]+(?:\s+[a-z0-9-]+){0,2})\b", re.IGNORECASE),
    re.compile(r"\b(siemens\s+s7-\d{3,4})\b", re.IGNORECASE),
    re.compile(r"\b(ubiquiti\s+[a-z0-9-]+(?:\s+[a-z0-9-]+){0,2})\b", re.IGNORECASE),
]

_FIRMWARE_PATTERNS = [
    re.compile(r"\bfirmware(?:\s+version)?[:\s]+v?(\d+(?:\.\d+){1,3})\b", re.IGNORECASE),
    re.compile(r"\bfw[:\s]+v?(\d+(?:\.\d+){1,3})\b", re.IGNORECASE),
    re.compile(r"\bversion[:\s]+(\d+(?:\.\d+){1,3})\b", re.IGNORECASE),
]

_GENERIC_MODEL_SUFFIXES = [
    "network camera",
    "device server",
    "video stream gateway",
    "camera",
    "gateway",
]


class _HTMLFingerprintParser(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._in_title = False
        self.title_chunks: list[str] = []
        self.metadata: dict[str, str] = {}

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr_map = {key.lower(): value for key, value in attrs if value}
        lowered_tag = tag.lower()
        if lowered_tag == "title":
            self._in_title = True
            return
        if lowered_tag != "meta":
            return

        key = (attr_map.get("name") or attr_map.get("property") or "").strip().lower()
        content = (attr_map.get("content") or "").strip()
        if key and content:
            self.metadata[key] = content

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "title":
            self._in_title = False

    def handle_data(self, data: str) -> None:
        if self._in_title:
            cleaned = data.strip()
            if cleaned:
                self.title_chunks.append(cleaned)


def parse_http_server_header(server_header: str | None) -> str | None:
    if server_header is None:
        return None
    cleaned = " ".join(server_header.strip().split())
    return cleaned or None


def parse_html_title_and_metadata(html: str | None) -> tuple[str | None, dict[str, str]]:
    if html is None or not html.strip():
        return None, {}

    parser = _HTMLFingerprintParser()
    parser.feed(html)
    title = " ".join(parser.title_chunks).strip() or None
    return title, dict(sorted(parser.metadata.items()))


def detect_device_model_hint(*values: str | None) -> str | None:
    for value in values:
        text = (value or "").strip()
        if not text:
            continue
        for pattern in _MODEL_PATTERNS:
            match = pattern.search(text)
            if match:
                candidate = " ".join(match.group(1).split())
                lowered = candidate.lower()
                for suffix in _GENERIC_MODEL_SUFFIXES:
                    if lowered.endswith(suffix):
                        candidate = candidate[: -len(suffix)].strip(" -")
                        break
                return candidate or None
    return None


def detect_firmware_version_hint(*values: str | None) -> str | None:
    for value in values:
        text = (value or "").strip()
        if not text:
            continue
        for pattern in _FIRMWARE_PATTERNS:
            match = pattern.search(text)
            if match:
                return match.group(1)
    return None


def build_web_fingerprint(
    server_header: str | None,
    html: str | None,
    favicon_bytes: bytes | None,
) -> dict[str, object]:
    normalized_server = parse_http_server_header(server_header)
    html_title, html_metadata = parse_html_title_and_metadata(html)
    model_hint = detect_device_model_hint(normalized_server, html_title, *html_metadata.values())
    firmware_hint = detect_firmware_version_hint(normalized_server, html_title, *html_metadata.values())
    favicon_hash = favicon_mmh3_from_bytes(favicon_bytes) if favicon_bytes else None

    return {
        "http_server": normalized_server,
        "html_title": html_title,
        "html_metadata": html_metadata,
        "favicon_hash": favicon_hash,
        "model_hint": model_hint,
        "firmware_hint": firmware_hint,
    }
