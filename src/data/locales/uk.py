from telebot.types import BotCommand

#? engine
from libs.bot_engine.languages.Locale import Locale


UK_LOCALE = Locale(
    language="uk",
    
    menu_commands=[
        BotCommand(command="start", description="Старт")
    ],

    messages= {
        "start": "Привiт, {}! Чудовий день, чи не так?",
    }
)
