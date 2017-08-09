from werkzeug.security import safe_str_cmp
from user import User

users = [
    User(1, 'tom', 'something fairly secure')
    # really only used for auth against the API - useless without the aws keys
]

username_map = {u.username: u for u in users}
user_id_map = {u.id: u for u in users}


def authenticate(username, password):
    user = username_map.get(username, None)
    if user and safe_str_cmp(user.password == password):
        return user


def identity(payload):
    user_id = payload['identity']
    return user_id_map.get(user_id, None)