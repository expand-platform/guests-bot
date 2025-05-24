from enum import Enum

#! Maybe I'll change them to numbers >0, >1 later
class AccessLevel(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    USER = "user"
    GUEST = "guest"


class CreateMethod(Enum):
    MESSAGE = "message"
    DATABASE = "database"


