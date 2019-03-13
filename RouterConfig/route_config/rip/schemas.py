rip_route_config_schema = {
    "title": "Rip Route Config Schema",
    "description": "schema of configuration which is used to config rip route",
    "type": "object",
    "properties": {
        "version": {"type": "number", "enum": [1, 2]},
        "networks": {
            "type": "array",
            "items": {
                "type": "string",
                "pattern": "^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/(?:[0-9]|[1-2][0-9]|3[1-2]?)$"
            }
        },
        "others": {
            "type": "array",
            "items": {"type": "string"}
        }
    },
    "additionalProperties": False
}
