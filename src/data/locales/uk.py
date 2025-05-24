from telebot.types import BotCommand

#? engine
from libs.bot_engine.languages.Locale import Locale

#? constats
from config.commands import BOT_COMMANDS

UK_LOCALE = Locale(
    language_name="uk",

    button_texts={},
    
    menu_commands=[
        BotCommand(command=BOT_COMMANDS.start, description="Старт")
    ],

    messages= {
        BOT_COMMANDS.start: "Привiт, {}! Чудовий день, чи не так?",
    }
)
