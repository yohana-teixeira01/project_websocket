from datetime import datetime
from functools import lru_cache

def get_current_datetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

@lru_cache(maxsize=None)
def calculate_fibonacci(n: int) -> int:
    if n <= 1:
        return n
    return calculate_fibonacci(n - 1) + calculate_fibonacci(n - 2)
