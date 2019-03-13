static_route_config_schema = {
    "title": "Static Route Config Schema",
    "description": "schema of configuration which is used to config static route",
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
                "required": ["next_hop", "dst_prefix"],
                "properties": {
                    "next_hop": {},
                    "dst_prefix": {
                        "type": "array",
                        "items": {
                            "type": "string",
                            "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:[0-9]|[1-2][0-9]|3[1-2]?)$"
                        }
                    }
                },
                "additionalProperties": False
            }
        ]
    }
}
