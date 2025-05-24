from dataclasses import dataclass

@dataclass
class BotCommands:
    start: str = "start"
    learn: str = "learn"
    ask: str = "ask"
    prices: str = "prices"
    about: str = "about"
    # learning_paths: str = "learning_paths"
    # languages: str = "languages"
    
BOT_COMMANDS = BotCommands()
