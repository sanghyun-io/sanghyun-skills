from dataclasses import dataclass

@dataclass
class User:
    id: int
    email: str
    password_hash: str

@dataclass
class Order:
    id: int
    user_id: int  # -> User.id
    total: int
    status: str  # pending | paid | cancelled
