from dataclasses import dataclass, field
from typing import Optional
from telebot.types import BotCommand


@dataclass
class Locale:
    language_name: str
    
    command_descriptions: dict[str, str] = field(default_factory=dict)

    messages: dict[str, str | list[str]] = field(default_factory=dict)
    button_texts: dict[str, list[str]] = field(default_factory=dict)

    #? auto-generated
    menu_commands: list[BotCommand] = field(default_factory=list, init=False)


    def __post_init__(self):
        self.generate_menu_commands()


    def generate_menu_commands(self):
        """ automatically create menu commands from command descriptions """
        for command, description in self.command_descriptions.items():
            self.menu_commands.append(
                BotCommand(command=command, description=description)
            )