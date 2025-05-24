from typing import Union, TYPE_CHECKING
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message, CallbackQuery

#? bot engine
from libs.bot_engine.enums.User import *

# ? engine types
if TYPE_CHECKING:
    from libs.bot_engine.database.Database import Database
    from libs.bot_engine.languages.Languages import Languages


#! для смены языка глобально можно каждый раз на этапе filter проверять активный язык юзера
class AccessLevelFilter(AdvancedCustomFilter):
    key = "access_level"

    def __init__(self, db: "Database", languages: "Languages"):
        self.database = db
        self.languages = languages


    def check(self, message: Union[Message, CallbackQuery], access_level: list[AccessLevel]):
        print(f"🔍 Filters (check)")
        active_user = None

        #? inline keyboard reply filters bot itself
        if not hasattr(message, "chat"):
            print(f"reply using inline keyboard from user { message.message.from_user.id }")
            active_user = self.database.get_active_user(message)
            message = message.message
        else: 
            active_user = self.database.get_active_user(message)

        user_access_level = active_user.access_level.value

        self.languages.set_active_language(active_user.language)

        access_level_values = [level.value for level in access_level]
        return user_access_level in access_level_values 
