# Bug type: type_error
# Description: String and integer concatenation causes TypeError

def build_message(username, score):
    return "Player " + username + " scored " + score + " points"