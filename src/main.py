# ? configs
from config.langConfig import DEFAULT_LANGUAGE
from config.env import DATABASE_TOKEN, SUPER_ADMIN_ID, ADMIN_IDS
from config.dbConfig import DATABASE_NAME
from config.langConfig import DEFAULT_LANGUAGE

# ? bot engine
from libs.bot_engine.bot.Bot import Bot
from libs.bot_engine.database.MongoDB import MongoDB
from libs.bot_engine.dialogs.DialogGenerator import DialogGenerator
from libs.bot_engine.languages.Languages import Languages
from libs.bot_engine.database.Database import Database
from libs.bot_engine.database.Cache import Cache

# ? engine customization
from bot.BotPlugins import MyBotPlugins
from server.Server import BotServer

# ? languages
from data.locales.uk import UK_LOCALE
from data.locales.ru import RU_LOCALE

# ? dialogs
from dialogs.AdminDialogs import AdminDialogs


# ? generic components

#! Кеш можно не создавать тут, а просто прокидывать настройки через higher-level класс  database
languages = Languages(DEFAULT_LANGUAGE)

# ? core parts
db = Database(DATABASE_TOKEN, DATABASE_NAME, SUPER_ADMIN_ID, ADMIN_IDS)
bot = Bot(db, languages)
dialogGenerator = DialogGenerator(bot, languages, db)
# BotDialogs = BotDialogs()

# Bot plugins and settings are created here
bot_configs = MyBotPlugins(
    languages=languages, db=db, bot=bot, dialogGenerator=dialogGenerator
)

#? 
bot_configs.set_languages(locales=[UK_LOCALE, RU_LOCALE], bot_language=DEFAULT_LANGUAGE)
bot_configs.set_database()

#? Slash commands and user dialogs
bot_configs.set_menu_commands()
bot_configs.set_bot_dialogs()


if __name__ == "__main__":
    server = BotServer(bot=bot)
    server.run()
