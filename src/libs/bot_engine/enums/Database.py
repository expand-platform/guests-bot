from enum import Enum


class DatabaseAdapter(Enum):
    MONGODB = "mongoDB"
    SQLITE = "SQLite"