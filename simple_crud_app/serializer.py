from typing import Optional
from dataclasses import dataclass

@dataclass
class UserCreateSerializer:
    username: str
    password: str
    first_name: str | None = None
    last_name: str | None = None
    
@dataclass
class UserLoginSerializer:
    id: int
    username: str
    password: str
    first_name: str
    lastname: str