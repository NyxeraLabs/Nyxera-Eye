# Copyright (c) 2026 NyxeraLabs
# Author: Jose Maria Micoli
# Licensed under BSL 1.1
# Change Date: 2033-02-17 -> Apache-2.0
#
# You may:
# - Study
# - Modify
# - Use for internal security testing
#
# You may NOT:
# - Offer as a commercial service
# - Sell derived competing products

from dataclasses import dataclass


@dataclass(slots=True)
class ChangeEvent:
    device_id: str
    change_type: str
    previous: str | None = None
    current: str | None = None


class DiffEngine:
    """Detects infrastructure state changes between snapshots."""

    def __init__(self) -> None:
        self._known_device_ids: set[str] = set()

    def diff(self, previous_devices: list[dict], current_devices: list[dict]) -> list[ChangeEvent]:
        previous_by_id = self._index_by_device_id(previous_devices)
        current_by_id = self._index_by_device_id(current_devices)

        events: list[ChangeEvent] = []

        for device_id, previous in previous_by_id.items():
            current = current_by_id.get(device_id)
            if current is None:
                events.append(ChangeEvent(device_id=device_id, change_type="device_disappeared"))
                continue

            if not self._is_vulnerable(previous) and self._is_vulnerable(current):
                events.append(
                    ChangeEvent(
                        device_id=device_id,
                        change_type="secure_to_vulnerable",
                        previous="secure",
                        current="vulnerable",
                    )
                )

            previous_firmware = self._firmware(previous)
            current_firmware = self._firmware(current)
            if previous_firmware and current_firmware and previous_firmware != current_firmware:
                events.append(
                    ChangeEvent(
                        device_id=device_id,
                        change_type="firmware_changed",
                        previous=previous_firmware,
                        current=current_firmware,
                    )
                )

        for device_id in current_by_id:
            if device_id not in previous_by_id and device_id in self._known_device_ids:
                events.append(ChangeEvent(device_id=device_id, change_type="device_reappeared"))

        self._known_device_ids.update(previous_by_id.keys())
        self._known_device_ids.update(current_by_id.keys())
        return events

    @staticmethod
    def _index_by_device_id(devices: list[dict]) -> dict[str, dict]:
        indexed: dict[str, dict] = {}
        for device in devices:
            device_id = str(device.get("device_id", "")).strip()
            if device_id:
                indexed[device_id] = device
        return indexed

    @staticmethod
    def _is_vulnerable(device: dict) -> bool:
        vulnerabilities = device.get("vulnerabilities", [])
        return bool(vulnerabilities)

    @staticmethod
    def _firmware(device: dict) -> str | None:
        metadata = device.get("iot_metadata", {}) or {}
        firmware = metadata.get("firmware")
        if firmware is None:
            return None
        normalized = str(firmware).strip()
        return normalized or None
