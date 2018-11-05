ospf_route_config_schema = {
    "title": "Ospf Route Config Schema",
    "description": "schema of configuration which is used to config ospf route",
    "type": "object",
    "anyOf": [
        {
            "properties": {},
            "minProperties": 0,
            "maxProperties": 0
        },
        {
            "properties": {
                "networks": {
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
                                "required": ["network", "area"],
                                "properties": {
                                    "network": {
                                        "type": "string",
                                        "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:[0-9]|[1-2][0-9]|3[1-2]?)$"
                                    },
                                    "area": {"type": "number"}
                                }
                            }
                        ]
                    }
                },
                "others": {
                    "type": "array",
                    "items": {"type": "string"}
                }
            },
            "additionalProperties": False
        }
    ]
}
