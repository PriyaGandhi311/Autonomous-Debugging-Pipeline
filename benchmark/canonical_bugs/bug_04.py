# Bug type: exception_handling
# Description: Bare except clause swallows all errors silently

def parse_config(config_str):
    try:
        import json
        return json.loads(config_str)
    except:
        return {}