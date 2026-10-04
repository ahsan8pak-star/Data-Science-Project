import re

def search(arr: list[int] | None, target: int) -> bool:
    if arr is None or len(arr) == 0:
        raise ValueError("Input array is null or empty")

    for i in arr:

        if i == target:
            return True

    return False

def sanitize_input(user_input: str) -> str:
    return re.sub(r"[^a-zA-Z0-9]", "", user_input)

