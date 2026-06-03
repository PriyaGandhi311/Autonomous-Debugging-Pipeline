# Bug type: return_type
# Description: Function returns 0 instead of empty dict on failure

def get_user_scores(user_id, scores_db):
    if user_id not in scores_db:
        return 0
    return scores_db[user_id]