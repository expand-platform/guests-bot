from dataclasses import dataclass, field

from libs.bot_engine.bot.BotConfigs import BotPlugins

#? engine customization
from dialogs.UserDialogs import UserDialogs
from dialogs.AdminDialogs import AdminDialogs

@dataclass
class MyBotPlugins(BotPlugins):

    def set_bot_dialogs(self):
        """ Prepares user and admin dialogs """
        UserDialogs(self.bot, self.dialogGenerator, self.languages).create_dialogs()
        AdminDialogs(self.bot, self.dialogGenerator, self.languages).create_dialogs()


