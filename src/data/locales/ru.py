from dataclasses import dataclass
from telebot.types import BotCommand
#? bot engine
from libs.bot_engine.languages.Locale import Locale

#? constats
from config.commands import BOT_COMMANDS
from config.buttons import BOT_BUTTONS



RU_LOCALE = Locale(
    language_name="ru",

    command_descriptions = {
        BOT_COMMANDS.start: "Старт",
        BOT_COMMANDS.btc_price: "Цена Bitcoin",       
    },

    button_texts = {
    },

    messages= { 
        BOT_COMMANDS.start: [
            "Привет! Я - бот-помощник по трейдингу",
        ], 
    }
)
