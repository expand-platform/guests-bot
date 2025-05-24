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
        """ 
            Use self.dialog_generator to generate user / admin dialogs.
            
            Example: 
            self.DialogGenerator.make_dialog(...) (see templates)
        """
        #! Разделить message в Language на userMessages и adminMessages
        messages = self.languages.get_messages()
        button_texts = self.languages.get_button_texts()
        
        #? /start: просит выбрать пункт меню
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.start,
            first_message=messages[BOT_COMMANDS.start],
        )
        
        #? /learn: просит выбрать пункт меню
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.learn,
            first_message=messages[BOT_COMMANDS.learn],
        )
        
        #? /about: о платформе
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.about,
            first_message=messages[BOT_COMMANDS.about],
        )
        
        #? /prices: цены на обучение
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.prices,
            first_message=messages[BOT_COMMANDS.prices],
        )
        
        #? /ask: задать вопрос
        self.dialogGenerator.make_dialog(
            command_name=BOT_COMMANDS.ask,
            first_message=messages[BOT_COMMANDS.ask],
        )

        # self.dialogGenerator.make_dialog(
        #     handler_type=HandlerType.SLASH_COMMAND,
        #     message_text=messages[BOT_COMMANDS.start],
        #     inline_button_texts=button_texts[BOT_BUTTONS.languages],
        #     inline_buttons_callback_property=CallbackProperties.language,
        #     active_state=None,
        #     save_to_state=None,
        # )

       