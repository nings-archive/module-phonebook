import random, string, time
from typing import Tuple

def random_group_rows() -> Tuple[Tuple[str, str, int, int], ...]:
    length = random.randint(1, 50)
    codes = tuple(set(random_module_code() for _ in range(length)))
    urls = tuple(set(random_url() for _ in range(length)))
    length_min = min(len(codes), len(urls))
    params = zip(codes[:length_min], urls[:length_min])
    rows = tuple(random_group_row(code, url) for code, url in params)
    return rows

def random_user_row() -> Tuple[int, int, int]:
    return random_user_id(), random.randint(0, 30), random.randint(0, 10)

def random_group_row(code:str=None, url:str=None) -> Tuple[str, str, int, int]:
    return (
        code if code else random_module_code(),
        url if url else random_url(),
        random_user_id(),
        random.randint(round(time.time()) + 60, 4102444800)
    )

def random_stats() -> Tuple[int, int, str]:
    return (random_user_id(), round(time.time()), random_command())

def random_user_id() -> int:
    """Generates a random user id"""
    return random.randint(200000000, 299999999)

def random_module_code() -> str:
    """Generates a random module code"""
    prefix = tuple(random_letter() for _ in range(random.randint(2, 3)))
    numeric = tuple(random_numeric_char() for _ in range(4))
    suffix = tuple(random_letter() for _ in range(random.randint(0, 1)))
    return ''.join(prefix + numeric + suffix)

def random_command() -> str:
    return ''.join(
        random.choice(string.ascii_lowercase)
        for _ in range(random.randint(1, 10))
    )

def random_url() -> str:
    """Generates a random URL"""
    return 'https://t.me/joinchat/{}'.format(
        ''.join(random.choice(string.ascii_letters) for _ in range(22))
    )

def random_numeric_char() -> str:
    """Generates a random number (as a string)"""
    return str(random.randint(0, 9))

def random_letter() -> str:
    """Generates a random (uppercase) letter"""
    return random.choice(string.ascii_uppercase)
