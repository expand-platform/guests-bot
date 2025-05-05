from dataclasses import dataclass, field
from typing import Any


#! Нужно будет создать базоый класс Adapter для работы с MongoDB / Sqlite / другими DB
@dataclass
class DatabaseAdapter:
    """ Adapter for different types of database"""
    pass

