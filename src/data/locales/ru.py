from dataclasses import dataclass
from telebot.types import BotCommand
#? bot engine
from libs.bot_engine.languages.Locale import Locale

#? constats
from config.commands import BOT_COMMANDS
from config.buttons import BOT_BUTTONS


#! Постараться к каждой команде закрепить ссылочку на Notion для деталей

@dataclass
class NotionPages:
    start: str = "https://expnd.notion.site/welcome"
    prices: str = "https://expnd.notion.site/prices"
    about: str = "https://expnd.notion.site/about"

NOTION_PAGE = NotionPages()


RU_LOCALE = Locale(
    language_name="ru",
    
    menu_commands=[
        BotCommand(command=BOT_COMMANDS.start, description="Старт"),
        BotCommand(command=BOT_COMMANDS.about, description="Куда я попал?"),
        BotCommand(command=BOT_COMMANDS.learn, description="Начать обучение"),
        BotCommand(command=BOT_COMMANDS.prices, description="Цены"),
        BotCommand(command=BOT_COMMANDS.ask, description="Задать вопрос"),
    ],

    button_texts = {
        BOT_BUTTONS.languages: ["Русский", "Украинский"],
    },

    messages= { 
        BOT_COMMANDS.start: [
            "👋 Welcome! Ты попал на платформу EXPAND — дом всех программистов и людей, которые любят IT.",

            "Меня зовут Дамир, я — full stack разработчик на Vue и Python, преподаватель, автор курсов и Ютуб-канала «Платформа EXPAND» ",
            "🤖 Это - мой бот для гостей платформы",

            f"📚 1. Если ты ищешь классные обучающие материалы, смотри /{BOT_COMMANDS.learn}",
            f"💁‍♂️ 2. Если нужна личная помощь, жми /{BOT_COMMANDS.ask}",
            f"🌓 3. Если ты ищешь наставника и ментора, чтобы связать свою судьбу с программированием и IT, тебе в /{BOT_COMMANDS.prices}",  
        ], 

       
        
        #? Расписать о направлениях, оставить ссылки на курсы
        BOT_COMMANDS.learn: [   
            "На платформе EXPAND можно изучить:",
            "1. HTML / CSS",
            "2. JavaScript",
            "3. VueJS и ReactJS",
            "4. Python",
            "5. C++",
            "⭐ Начать обучение можно прямо сейчас. Платить ничего не нужно:",
            f"{NOTION_PAGE.start}",
        ],

        
        BOT_COMMANDS.prices: [""
        "🔗 Все цены находятся по ссылке:",
        f"{NOTION_PAGE.prices}",
        ],


        BOT_COMMANDS.ask: [
            "🌗 Ты можешь задать вопрос мне лично:",
            "@best\\_prepod",
        ],

         BOT_COMMANDS.about: [
            "⭐ «EXPAND» — это онлайн-школа, курсы и моё авторское обучение программированию. "
            "К нам приходят люди, которые любят писать код и хотят работать в IT", 
            
            "⭐ Ты можешь пройти курс по HTML / CSS, JavaScript (Vue и React), Python, PHP и стать фронтенд или бекенд-разработчиком.",

            "⭐ Я лично готовлю все материалы, видео, задачи и проекты — и стараюсь делать их интересно, с душой и изюминкой",

            "⭐ Ты можешь начать обучение прямо сейчас, за это не нужно платить деньги:",
            f"{NOTION_PAGE.start}",
        ], 
        
        # BOT_COMMANDS.languages: "Выбери язык / обери мову", 
    }
)
