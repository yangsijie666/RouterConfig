bgp_route_config_schema = {
    "title": "Bgp Route Config Schema",
    "description": "schema of configuration which is used to config bgp route",
    "type": "object",
    "oneOf": [
        {
            "properties": {},
            "minProperties": 0,
            "maxProperties": 0
        },
        {
            "required": ["as_num"],
            "properties": {
                "as_num": {"type": "number"},
                "network": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:[0-9]|[1-2][0-9]|3[1-2]?)$"
                    }
                },
                "ebgp_neighbors": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "oneOf": [
                            {
                                "properties": {},
                                "minProperties": 0,
                                "maxProperties": 0
                            },
                            {
                                "required": ["neighbor_ip", "neighbor_as"],
                                "properties": {
                                    "neighbor_ip": {
                                        "type": "string",
                                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                                    },
                                    "neighbor_as": {"type": "number"}
                                },
                                "additionalProperties": False
                            }
                        ]
                    }
                },
                "ibgp_neighbors": {
                    "type": "array",
                    "items": {
                        "type": "string",
                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
                    }
                },
                "others": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "additionalProperties": False
        }
    ]
}