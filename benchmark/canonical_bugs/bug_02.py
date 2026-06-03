# Bug type: null_check
# Description: Missing None check before accessing object attribute

def get_user_email(user):
    return user["email"].strip()