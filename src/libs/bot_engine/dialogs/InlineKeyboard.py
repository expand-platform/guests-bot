from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

class InlineKeyboard:
    def __init__(self):
        self.columns = 2
        self.keyboard = InlineKeyboardMarkup(row_width=self.columns)
        
    
    def show_yes_no_keyboard(self, yes_button_text, no_button_text, yes_button_callback, no_button_callback):
        # clear keyboard first
        self.keyboard = InlineKeyboardMarkup(keyboard=[])
        
        yes_button = InlineKeyboardButton(text=yes_button_text, callback_data=yes_button_callback)
        no_button = InlineKeyboardButton(text=no_button_text, callback_data=no_button_callback)
        
        self.keyboard.add(yes_button, no_button)
           