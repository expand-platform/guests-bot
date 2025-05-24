from dataclasses import dataclass, field
from telebot.types import BotCommand


@dataclass
class Locale:
    language_name: str
    menu_commands: list[BotCommand]
    messages: dict[str, str | list[str]]
    button_texts: dict[str, list[str]]