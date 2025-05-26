#? bot engine
from libs.bot_engine.dialogs.BotDialogs import BotDialogs
from libs.bot_engine.enums.User import AccessLevel
from libs.bot_engine.enums.Generator import *

#? constants
from config.commands import BOT_COMMANDS
from config.buttons import BOT_BUTTONS

#? enums
from config.CallbackProperties import CallbackProperties


#! 1. Первая юзерская команда будет /add (добавить товар для отслеживания) 
#! 2. Вторая команда - /bulkadd (добавить много товаров для отслеживания) 

class UserDialogs(BotDialogs):
    """ creates user dialogs """

    
    #! 3. Здесь делаем эти самые команды-диалоги
    def create_dialogs(self):
        """ create dialogs using dialog generator """
        messages = self.languages.get_messages()
        button_texts = self.languages.get_button_texts()
        
        #? /start: просит выбрать пункт меню
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.start,
            first_message=messages[BOT_COMMANDS.start],
        )
        
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.btc_price,
            first_message=messages[BOT_COMMANDS.btc_price],
        )


        
      

       