from dotenv import dotenv_values



class Dotenv:
    def __init__(self):
        config = dotenv_values(".env")  
        print("🐍 File: helpers/Dotenv.py | Line: 8 | __init__ ~ config",config)
        # load_dotenv()

        # self.bot_token = ""

        # self.user_ids = []

        # self.environment = ""
        # self.mongodb_string = ""

        # self.collect_env_data()

    # def collect_env_data(self):
        # self.bot_token: str = os.getenv("BOT_TOKEN")

        # self.user_ids: list[int] = self.convert_to_list(os.getenv("USER_IDS"))

        # self.environment: str = os.getenv("ENVIRONMENT")
        # self.mongodb_string: str = os.getenv("MONGODB_STRING")

    # def convert_to_list(self, env_variable: str):
        # list = env_variable.split(",")
        # return [int(item) for item in list]
