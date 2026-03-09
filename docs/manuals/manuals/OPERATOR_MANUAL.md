<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# Operator Manual

## Mission

Use Nyxera Eye to discover, enrich, review, and investigate exposed assets within authorized scope.

## Standard Workflow

1. Open the dashboard and run a single scan to seed the inventory.
2. Start the scan loop to accumulate additional assets over time.
3. Review severity, status, vendor, port, and country charts.
4. Open `/devices` and filter by vendor, country, severity, or free text.
5. Open `/findings` and filter by severity or status.
6. Investigate a finding into `/devices/{deviceId}`.
7. Review audit events after notable actions.

## Device Investigation Expectations

Each device detail should show:

- stable device identity
- IP, city, and country
- severity and scan count
- services and banners
- web fingerprint fields
- vendor, model, and firmware hints
- linked finding
- recent events

## Safety Requirements

Never use the platform for:

- brute force
- exploitation
- intrusive probing outside approved scope

Passive mode is the default. Authorized scope mode must be explicitly configured and logged.
