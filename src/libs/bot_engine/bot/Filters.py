from typing import Union, TYPE_CHECKING
from telebot.custom_filters import AdvancedCustomFilter
from telebot.types import Message, CallbackQuery

# ? engine types
if TYPE_CHECKING:
    from libs.bot_engine.database.Database import Database
    from libs.bot_engine.languages.Languages import Languages


#! для смены языка глобально можно каждый раз на этапе filter проверять активный язык юзера
class AccessLevelFilter(AdvancedCustomFilter):
    key = "access_level"

    def __init__(self, db: "Database", languages: "Languages"):
        self.db = db

    def check(self, message: Union[Message, CallbackQuery], access_level: str):
        print(f"Filters (check)")

        # ? if user replies with a keyboard
        if not hasattr(message, "chat"):
            print(f"no message.chat found: { message.message.chat.id }")
            message = message.message

        active_user = self.db.get_active_user(message)
        user_access_level = active_user.access_level.value
        print("🐍 user_access_level: ",user_access_level)

        #! На этом этапе можно пробовать задавать активный язык юзера
        #? Languages.set_active_lang from active_user.language

        #? check a list of values or a single value
        if isinstance(access_level, list):
            print("if", user_access_level in access_level)
            return user_access_level in access_level
        else:
            print("else", user_access_level == access_level)
            return user_access_level == access_level
