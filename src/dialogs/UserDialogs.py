#? bot engine
from libs.bot_engine.dialogs.BotDialogs import BotDialogs


#! 1. Первая юзерская команда будет /add (добавить товар для отслеживания) 
#! 2. Вторая команда - /bulkadd (добавить много товаров для отслеживания) 

class UserDialogs(BotDialogs):
    """ creates user dialogs """

    
    #! 3. Здесь делаем эти самые команды-диалоги
    def create_dialogs(self):
        """ 
            Use self.dialog_generator to generate user / admin dialogs.
            
            Example: 
            self.DialogGenerator.make_dialog(...) (see templates)
        """
        messages = self.language.get_messages()

        self.dialogGenerator.make_dialog(
            access_level=["user"],
            handler_type="command",
            command_name="start",
            
            #! Разделить на userMessages и adminMessages
            bot_before_message=messages["start"],
        )