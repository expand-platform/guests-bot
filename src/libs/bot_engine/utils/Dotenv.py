from dotenv import load_dotenv
from os import getenv


class Dotenv:
    def __init__(self):
        load_dotenv()

    def get(self, key_name: str) -> str | None:
        value = getenv(key=key_name)
        if value is None:
            print(f"🔴 CRITICAL: you must set the key '{key_name}' in your .env file!")
        return value


    def get_int(self, key_name: str) -> int:
        value = self.get(key_name)
        return int(value) if value is not None else 0


    def get_list_of_ints(self, key_name: str) -> list[int]:
        value = self.get(key_name)
        if value:
            return [int(item.strip()) for item in value.split(",")]
        return []


    def get_list_of_strs(self, key_name: str) -> list[str]:
        value = self.get(key_name)
        if value:
            return [item.strip() for item in value.split(",")]
        return []
