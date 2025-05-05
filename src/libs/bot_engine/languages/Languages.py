from os import getenv

from dataclasses import dataclass, field
from typing import ClassVar

from httpx import get
from telebot.types import BotCommand

#? engine
from libs.bot_engine.languages.Locale import Locale



@dataclass
class Languages:
    active_lang: str = "ru"
    languages: ClassVar[dict[str, Locale]] = {}
    messages: ClassVar[dict[str, str]] = {}


    def add_locale(self, locale: Locale):
        self.languages[locale.language] = locale
        print(f"🔷 {locale.language} is added to languages!")


    def get_active_locale(self) -> Locale | None:
        return self.languages.get(self.active_lang)
    

    def get_menu_commands(self, user_language: str | None = None) -> list[BotCommand]:
        active_language = user_language or self.active_lang
        locale = self.languages.get(active_language)

        if not locale:
            raise ValueError(f"Locale {active_language} not found.")
        
        return locale.menu_commands


    def get_messages(self, user_language: str | None = None) -> dict[str, str]:
        active_language = user_language or self.active_lang
        locale = self.languages.get(active_language)

        if not locale:
            raise ValueError(f"Locale '{active_language}' not found.")
        
        return locale.messages

    def set_messages(self, language: str | None = None):
        Languages.messages = self.get_messages(language or self.active_lang)
