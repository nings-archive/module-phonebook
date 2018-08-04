from dataclasses import dataclass
from typing import Union

@dataclass(frozen=True)
class User:
    user_id: int
    state: int
    role: int
    saved_state: Union[str, None] = None

@dataclass(frozen=True)
class Group:
    code: str
    url: str
    owner: int
    expiry: int
