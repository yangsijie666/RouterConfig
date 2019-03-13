data_filter_schema = {
    "title": "Data Filter Schema",
    "description": "schema of configuration which is used to filter data",
    "type": "object",
    "properties": {
        "source_mac": {
            "type": "string",
            "pattern": "^[0-9a-fA-F]{2}(:[0-9a-fA-F]{2}){5}$"
        },
        "ip_address": {
            "type": "object",
            "properties": {
                "src": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                    }
                },
                "dst": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                    }
                }
            }
        },
        "port": {
            "type": "object",
            "properties": {
                "src": {"type": "string"},
                "dst": {"type": "string"}
            }
        },
        "protocol": {"type": "string", "enum": ["all", "tcp", "udp", "icmp"]},
        "nic": {
            "type": "object",
            "properties": {
                "in": {"type": "string"},
                "out": {"type": "string"}
            }
        }
    },
    "additionalProperties": False
}
