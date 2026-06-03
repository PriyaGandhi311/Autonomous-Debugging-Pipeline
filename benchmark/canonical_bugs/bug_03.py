# Bug type: off_by_one
# Description: Loop goes out of bounds by one index

def get_last_n_items(items, n):
    result = []
    for i in range(len(items) - n, len(items) + 1):
        result.append(items[i])
    return result