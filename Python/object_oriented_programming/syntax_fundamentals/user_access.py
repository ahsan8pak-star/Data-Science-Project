def login_check(username, password):
    user_db = {
        'user1': 'password123',
        'user2': 'securepass',
    }
    return username in user_db and user_db[username] == password


def permission_check(username, action):
    permissions = {
        'user1': ['read', 'write'],
        'user2': ['read'],
    }
    return username in permissions and action in permissions[username]


def require_login(func):
    def wrapper(username, password, action):
        if not login_check(username, password):
            return "Invalid username or password."
        return func(username, password, action)
    return wrapper


def require_permission(action_name):
    def decorator(func):
        def wrapper(username, password, action):
            if not permission_check(username, action_name):
                return f"Access denied for {username}. Insufficient permissions for {action_name}."
            return func(username, password, action)
        return wrapper
    return decorator


@require_login
@require_permission("write")
def user_access(username, password, action):
    return f"Access granted for {username} to perform {action}."

user1_access = user_access("user1", "password123", "write")
user2_access = user_access("user2", "securepass", "read")

print(user1_access)  # Output: Access granted for user1 to perform write.
print(user2_access)  # Output: Access denied for user2. Insufficient permissions for write.

