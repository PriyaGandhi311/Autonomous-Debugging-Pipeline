# Bug type: return_type
# Description: Function returns None instead of empty list when no items found

def get_active_users(users):
    active = []
    for user in users:
        if user["is_active"]:
            active.append(user["name"])
    if len(active) == 0:
        return None
    return active