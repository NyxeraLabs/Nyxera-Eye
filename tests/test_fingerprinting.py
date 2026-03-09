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

from nyxera_eye.clustering.certificate_correlation import correlate_by_certificate_serial
from nyxera_eye.fingerprinting.ja3 import build_ja3_string, ja3_hash
from nyxera_eye.fingerprinting.jarm import jarm_fingerprint
from nyxera_eye.fingerprinting.murmurhash3 import murmurhash3_x86_32


def test_murmurhash3_known_vector() -> None:
    assert murmurhash3_x86_32(b"hello") == 613153351


def test_ja3_string_and_hash() -> None:
    ja3 = build_ja3_string(
        tls_version=771,
        ciphers=[4865, 4866],
        extensions=[0, 11, 10],
        elliptic_curves=[29, 23],
        ec_point_formats=[0],
    )

    assert ja3 == "771,4865-4866,0-11-10,29-23,0"
    assert len(ja3_hash(ja3)) == 32


def test_jarm_fingerprint_is_deterministic() -> None:
    probes = ["tls1.2:4865", "tls1.3:4866", "ext:sni"]
    fp_a = jarm_fingerprint(probes)
    fp_b = jarm_fingerprint(probes)

    assert fp_a == fp_b
    assert len(fp_a) == 64


def test_certificate_serial_correlation_groups_ips() -> None:
    records = [
        {"certificate_serial": "ABC123", "ip": "203.0.113.10"},
        {"certificate_serial": "ABC123", "ip": "203.0.113.11"},
        {"certificate_serial": "XYZ999", "ip": "198.51.100.20"},
    ]

    clusters = correlate_by_certificate_serial(records)

    assert clusters["ABC123"] == ["203.0.113.10", "203.0.113.11"]
    assert clusters["XYZ999"] == ["198.51.100.20"]
