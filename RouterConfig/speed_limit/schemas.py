speed_limit_schema = {
    "title": "Speed Limit Schema",
    "description": "schema of configuration which is used to speed limit",
    "type": "object",
    "required": ["nic", "speed"],
    "properties": {
        "nic": {"type": "string"},
        "speed": {
            "type": "string",
            "pattern": "^[1-9][kmgt]bit$|^[1-9]bit$|^[1-9]\d+bit$|^[1-9]\d+[kmgt]bit$|^[1-9][kmgt]bps$|^[1-9]bps$|^[1-9]\d+bps$|^[1-9]\d+[kmgt]bps$"
        }
    }
}
