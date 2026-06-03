# Bug type: null_check
# Description: Chained attribute access without null guard

def get_city(order):
    return order["customer"]["address"]["city"]