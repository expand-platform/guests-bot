#? bot engine
from libs.bot_engine.utils.Dotenv import Dotenv

dotenv = Dotenv()

ENVIRONMENT: str = dotenv.get("ENVIRONMENT") or "DEVELOPMENT" 
PORT: int = dotenv.get_int("PORT") or 8000

BOT_TOKEN: str = dotenv.get("BOT_TOKEN") or "" 
DATABASE_TOKEN: str = dotenv.get("DATABASE_TOKEN") or "" 

SUPER_ADMIN_ID: int = dotenv.get_int("SUPER_ADMIN_ID")
ADMIN_IDS: list[int] = dotenv.get_list_of_ints("ADMIN_IDS")
# USER_IDS: list[int] = dotenv.get_list_of_ints("USER_IDS")
