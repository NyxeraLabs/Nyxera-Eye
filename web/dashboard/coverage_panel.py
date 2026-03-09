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

from html import escape


def render_coverage_panel(snapshot: dict[str, object]) -> str:
    return (
        '<section class="coverage-panel">'
        "<h2>Scan Coverage</h2>"
        f"<p>Queued Targets: {escape(str(snapshot.get('queued_targets', 0)))}</p>"
        f"<p>Eligible Targets: {escape(str(snapshot.get('eligible_targets', 0)))}</p>"
        f"<p>Skipped Due To Cooldown: {escape(str(snapshot.get('skipped_due_to_cooldown', 0)))}</p>"
        f"<p>Sampled Targets: {escape(str(snapshot.get('sampled_targets', 0)))}</p>"
        f"<p>Coverage Ratio: {escape(str(snapshot.get('coverage_ratio', 0)))}</p>"
        "</section>"
    )
