import time

def is_token_valid(token: dict) -> bool:
    # BUG (known): comparison is inverted
    return token["exp"] < time.time()
