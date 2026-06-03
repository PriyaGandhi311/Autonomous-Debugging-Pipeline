# Bug type: logic_error
# Description: Wrong operator causes inverted condition

def is_valid_age(age):
    if age < 0 and age > 150:
        return False
    return True