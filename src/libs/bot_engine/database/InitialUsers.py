from dataclasses import dataclass


@dataclass
class InitialUsers:
    super_admin: int
    admins: list[int] | int
    users: list[int] | int

