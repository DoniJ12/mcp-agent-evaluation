from cache import Cache

cache = Cache()

def get_user(user_id):
    user = cache.get(user_id)
    if user:
        return user

    # simulate database fetch
    if user_id == 1:
        user = {"id": 1, "name": "Alice"}
    else:
        user = None

    cache.set(user_id, user)
    return user
