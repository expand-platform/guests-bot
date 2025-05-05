#? bot engine
from libs.bot_engine.dialogs.BotDialogs import BotDialogs


class AdminDialogs(BotDialogs):
    """ creates admin dialogs """
    def create_dialogs(self):
        """ 
            Use self.dialog_generator to generate user / admin dialogs.
            
            Example: 
            self.DialogGenerator.make_dialog(...) (see templates)
        """
        messages = self.language.get_messages()

        self.dialogGenerator.make_dialog(
            access_level=["admin", "super_admin"],
            handler_type="command",
            command_name="start",
            
            # formatted_variables=[]
            bot_before_message=messages["start"],
        )
        
