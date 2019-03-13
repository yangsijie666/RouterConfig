route_config_schema = {
    "title": "Route Config Schema",
    "description": "schema of configuration which is used to config route",
    "type": "object",
    "properties": {
        "static": {
            "type": "array",
            "items": {"default": {}}
        },
        "rip": {
            "type": "object",
            "properties": {"default": {}}
        },
        "ospf": {
            "type": "object",
            "properties": {"default": {}}
        },
        "bgp": {
            "type": "object",
            "properties": {"default": {}}
        }
    }
}
