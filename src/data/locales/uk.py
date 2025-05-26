from dataclasses import dataclass
from telebot.types import BotCommand
#? bot engine
from libs.bot_engine.languages.Locale import Locale

#? constats
from config.commands import BOT_COMMANDS
from config.buttons import BOT_BUTTONS


UK_LOCALE = Locale(
    language_name="uk",

    command_descriptions = {
        BOT_COMMANDS.start: "Старт",
        BOT_COMMANDS.btc_price: "Ціна Bitcoin",     
    },

    button_texts = {
    },

    messages= { 
        BOT_COMMANDS.start: [
            "Привiт! Я - бот-помiчник для трейдингу",
        ], 
        BOT_COMMANDS.btc_price: [
            "Цiна Bitcoin зараз: ",
        ], 
    }
)