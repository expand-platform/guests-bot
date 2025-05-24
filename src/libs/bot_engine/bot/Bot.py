from __future__ import annotations
from typing import Optional, Union, TYPE_CHECKING
from dataclasses import dataclass, field

from click import Option
from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup
from telebot.states.sync.middleware import StateMiddleware
from telebot.custom_filters import StateFilter, IsDigitFilter, TextMatchFilter

#? bot engine
from libs.bot_engine.database.Database import Database
from libs.bot_engine.bot.Filters import AccessLevelFilter
from config.env import (
    ENVIRONMENT,
    BOT_TOKEN,
    ADMIN_IDS,
    SUPER_ADMIN_ID,
)
from libs.bot_engine.languages.Languages import Languages

#? const / enums
from libs.bot_engine.const.Bot import * 


@dataclass
class Bot:
    db: Database
    languages: Languages
    _bot: TeleBot = field(init=False)


    def __post_init__(self):
        self._bot = TeleBot(token=BOT_TOKEN, use_class_middlewares=True)


    def start(self) -> TeleBot:
        if self._bot:
            self.set_middleware()
            self.tell_super_admin(["Начинаю работу...", "/start"])

        bot_username = self.get_bot_data("username")
        print(f"🟢 Бот @{bot_username} подключён! Нажми /start для начала")

        self._bot.infinity_polling(
            timeout=5,
            skip_pending=True,
            long_polling_timeout=20,
            restart_on_change=(ENVIRONMENT in ["testing", "development"]),
        )

        return self._bot


    def disconnect(self) -> None:
        self._bot.stop_bot()
        print("бот выключен ❌")


    def get_bot_data(self, requested_data: str) -> str:
        all_bot_info = self._bot.get_me()
        return getattr(all_bot_info, requested_data)


    def set_middleware(self) -> None:
        self._bot.add_custom_filter(StateFilter(self._bot))
        self._bot.add_custom_filter(IsDigitFilter())
        self._bot.add_custom_filter(TextMatchFilter())
        self._bot.add_custom_filter(AccessLevelFilter(self.db, self.languages))

        self._bot.setup_middleware(StateMiddleware(self._bot))


    def tell_admins(self, messages: Union[str, list[str]]):
        for admin_id in ADMIN_IDS:
            self._send_message(chat_id=admin_id, messages=messages)


    def tell_super_admin(self, messages: str | list[str]):
        self._send_message(chat_id=SUPER_ADMIN_ID, messages=messages)


    def _send_message(
        self,
        chat_id: int,
        messages: str | list[str],

        format_variables: Optional[str | int | list] = None,
        reply_markup: Optional[InlineKeyboardMarkup] = None,

        parse_mode=ParseMode.MARKDOWN,
        disable_preview: Optional[bool] = False,
    ):
        """ sends one or multiple messages. Supports format variables (1 message = 1 var) """
        if isinstance(messages, str):
            messages = [messages]

        if isinstance(format_variables, (str, int)):
            format_variables = [format_variables]

        if format_variables:
            for message, format_variable in zip(messages, format_variables):
                self._bot.send_message(
                    chat_id=chat_id,
                    text=message.format(format_variable),
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_preview,
                )
        else:
            for message in messages:
                self._bot.send_message(
                    chat_id=chat_id,
                    text=message,
                    parse_mode=parse_mode,
                    reply_markup=reply_markup,
                    disable_web_page_preview=disable_preview,
                )
