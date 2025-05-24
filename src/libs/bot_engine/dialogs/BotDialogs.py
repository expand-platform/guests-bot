#? engine
from dataclasses import dataclass
from libs.bot_engine.bot.Bot import Bot
from libs.bot_engine.dialogs.DialogGenerator import DialogGenerator
from libs.bot_engine.languages.Languages import Languages

@dataclass
class BotDialogs:
    """
        Dependencies: 
        1. Bot (for sending messages)
        2. DialogGenerator
        3. Languages (for texts)
    """
    bot: Bot
    dialogGenerator: DialogGenerator
    languages: Languages


    def create_dialogs(self):
        """ 
            Use self.dialog_generator to generate user / admin dialogs.
            
            Example: 
            self.DialogGenerator.make_dialog(...) (see templates)
        """
        pass
