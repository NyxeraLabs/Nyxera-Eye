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

SHODAN_PAYLOAD = {
    "matches": [
        {
            "ip_str": "198.51.100.10",
            "port": 80,
            "transport": "tcp",
            "data": "HTTP/1.1 200 OK",
            "org": "Example ISP",
            "location": {"country_name": "Argentina"},
            "timestamp": "2026-03-01T10:00:00Z",
        }
    ]
}

CENSYS_PAYLOAD = {
    "result": {
        "hits": [
            {
                "ip": "203.0.113.44",
                "services": [
                    {
                        "port": 443,
                        "transport_protocol": "tcp",
                        "banner": "TLS service",
                    }
                ],
                "autonomous_system": {"description": "AS64500"},
                "location": {"country": "US"},
                "last_updated_at": "2026-03-01T10:05:00Z",
            }
        ]
    }
}

ZOOMEYE_PAYLOAD = {
    "matches": [
        {
            "ip": "192.0.2.77",
            "portinfo": {
                "port": 502,
                "transport": "tcp",
                "banner": "Modbus",
            },
            "geoinfo": {
                "organization": "Factory Net",
                "country": {"names": {"en": "Germany"}},
            },
            "timestamp": "2026-03-01T10:10:00Z",
        }
    ]
}
