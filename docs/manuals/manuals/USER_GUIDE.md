<!--
Copyright (c) 2026 NyxeraLabs
Author: Jose Maria Micoli
Licensed under BSL 1.1
Change Date: 2033-02-17 -> Apache-2.0
-->

# User Guide

## Overview

Nyxera Eye provides a live operator workflow for:

- discovering network assets
- accumulating service metadata across scan runs
- fingerprinting web-facing assets
- exposing vendor and firmware hints
- tracking findings and actions
- investigating devices from the UI

## Main Screens

- Dashboard: `/`
- Device registry: `/devices`
- Device investigation: `/devices/{deviceId}`
- Findings registry: `/findings`
- World map: `/map`
- Events: `/events`
- Settings: `/settings`
- Audit: `/audit`

## Typical Session

1. Authenticate.
2. Run a single scan from the dashboard.
3. Start the scan loop if you want inventory growth over time.
4. Review severity, vendor, port, and geography charts.
5. Search devices from `/devices`.
6. Review and filter findings from `/findings`.
7. Investigate into the device detail page.
8. Export a finding if needed.

## Runtime Model

- device inventory is cumulative
- findings persist across scan runs
- finding actions update status and history
- map coordinates are centered around major world cities

## Related Documents

- [../guides/GETTING_STARTED.md](../guides/GETTING_STARTED.md)
- [../guides/INSTALLATION.md](../guides/INSTALLATION.md)
- [API_MANUAL.md](API_MANUAL.md)
- [OPERATOR_MANUAL.md](OPERATOR_MANUAL.md)
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md)
