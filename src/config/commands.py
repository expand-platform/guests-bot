from dataclasses import dataclass, field
from typing import Optional



@dataclass
class BotCommands:
    start: str = "start"
    btc_price: str = "btc_price"

BOT_COMMANDS = BotCommands()
