from os import getenv
from typing import Optional
from dataclasses import dataclass, field
from typing import ClassVar

from httpx import get
from telebot.types import BotCommand

#? engine
from libs.bot_engine.languages.Locale import Locale



@dataclass
class Languages:
    active_lang: str = "ru"
    languages: list[str] = field(default_factory=list)
    messages: dict[str, dict[str, str]] = field(default_factory=dict)
    button_texts: dict[str, dict[str, list[str]]] = field(default_factory=dict)
    menu_commands: dict[str, list[BotCommand]] = field(default_factory=dict)


    def add_locale(self, locale: Locale):
        """ adds new language [Locale object] to languages """
        new_language = locale.language_name
        self.languages.append(new_language)
        self.messages[new_language] = locale.messages 
        self.button_texts[new_language] = locale.button_texts 
        self.menu_commands[new_language] = locale.menu_commands

        print(f"🔷 {new_language} is added to languages!")


    def set_active_language(self, new_language_name: str):
        """ sets a new active language used for retrieving texts """
        self.active_lang = new_language_name
        # print(f"active language now is: {self.active_lang}")


    def get_messages(self, user_language: Optional[str] = None) -> dict[str, str]:
        """ get message texts """
        active_language = user_language or self.active_lang
        return self.messages[active_language]
    

    def get_button_texts(self, user_language: Optional[str] = None) -> dict[str, list[str]]:
        """ get button texts """
        active_language = user_language or self.active_lang
        # print(f"button texts: {self.button_texts[active_language]}")
        return self.button_texts[active_language]
    
    def get_menu_commands(self, user_language: Optional[str] = None) -> list[BotCommand]:
        """ get button texts """
        active_language = user_language or self.active_lang
        return self.menu_commands[active_language]
    