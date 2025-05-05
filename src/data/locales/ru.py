from telebot.types import BotCommand
#? bot engine
from libs.bot_engine.languages.Locale import Locale

RU_LOCALE = Locale(
    language="ru",
    
    menu_commands=[
        BotCommand(command="start", description="Старт")
    ],

    messages=[
        { "start": "Привет, {}! Чудный день, не так ли?" }
    ]
)
