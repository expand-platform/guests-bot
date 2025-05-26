# ? configs
from api.api_client_name import API_CLIENTS
from config.langConfig import DEFAULT_LANGUAGE
from config.env import DATABASE_TOKEN, SUPER_ADMIN_ID, ADMIN_IDS
from config.dbConfig import DATABASE_NAME
from config.langConfig import DEFAULT_LANGUAGE

# ? bot engine
from libs.bot_engine.bot.Bot import Bot
from libs.bot_engine.dialogs.DialogGenerator import DialogGenerator
from libs.bot_engine.languages.Languages import Languages
from libs.bot_engine.database.Database import Database

# ? engine customization
from bot.BotPlugins import MyBotPlugins
from server.Server import BotServer

# ? languages
from data.locales.uk import UK_LOCALE
from data.locales.ru import RU_LOCALE 

# ? dialogs
from dialogs.AdminDialogs import AdminDialogs

#? bot-specific settings (API etc)
from config.env import BINANCE_TOKEN, BINANCE_SECRET
from api.api import BinanceAPI


#? generic components
languages = Languages()

#? core parts
db = Database(DATABASE_TOKEN, DATABASE_NAME, SUPER_ADMIN_ID, ADMIN_IDS)
binance_client = BinanceAPI(TOKEN=BINANCE_TOKEN, SECRET=BINANCE_SECRET)
bot = Bot(db, languages)
dialogGenerator = DialogGenerator(bot, languages, db)


#? bot settings 
bot_plugins = MyBotPlugins(
    languages=languages, db=db, bot=bot, dialogGenerator=dialogGenerator
)


#? bot settings 
bot_plugins.add_api_client(client_name=API_CLIENTS.Binance, client=binance_client)
bot_plugins.set_languages(locales=[UK_LOCALE, RU_LOCALE], bot_language=DEFAULT_LANGUAGE)
bot_plugins.set_database()

#? Slash commands and user dialogs
bot_plugins.set_menu_commands()
bot_plugins.set_bot_dialogs()


if __name__ == "__main__":
    server = BotServer(bot=bot)
    server.run()
