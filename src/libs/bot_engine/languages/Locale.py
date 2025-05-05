from dataclasses import dataclass, field
from telebot.types import BotCommand


@dataclass
class Locale:
    language: str
    menu_commands: list[BotCommand]
    messages: dict[str, str]