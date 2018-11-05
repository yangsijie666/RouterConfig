main_schema = {
    "title": "Main Schema",
    "description": "schema of configuration which is used to all of the programs",
    "type": "object",
    "properties": {
        "route_config": {
            "type": "object",
            "properties": {"default": {}}
        },
        "data_filter": {
            "type": "array",
            "items": {"default": {}}
        },
        "congestion_control": {
            "type": "array",
            "items": {"default": {}}
        }
    },
    "default": {}
}
