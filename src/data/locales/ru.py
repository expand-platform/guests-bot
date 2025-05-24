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
        BOT_BUTTONS.languages: ["Русский", "Українська"],
    },

    messages= { 
        BOT_COMMANDS.start: [
            "👋 Welcome! Ты попал на платформу EXPAND — дом всех программистов",

            "Меня зовут Дамир, я — создатель «Платформы EXPAND»",

            f"📚 1. Если ты ищешь обучающие материалы по программированию, смотри /{BOT_COMMANDS.learn}",
            f"🌓 2. Если ты ищешь учителя / наставника, тебе в /{BOT_COMMANDS.prices}",  
            f"💁‍♂️ 3. Если нужна личная помощь, я тут: /{BOT_COMMANDS.ask}",
        ], 

       
        
        #? Расписать о направлениях, оставить ссылки на курсы
        BOT_COMMANDS.learn: [   
            "На платформе EXPAND можно изучить:\n\n1. HTML / CSS\n2. JavaScript\n3. VueJS и ReactJS\n4. Python\n5. C++\n",
            "⭐ Начать обучение можно прямо сейчас. За это не нужно платить:\n" 
            f"{NOTION_PAGE.start}",
        ],

        
        BOT_COMMANDS.prices: [""
        "🔗 Цены на групповые и индивидуальные занятия можно посмотреть тут:",
        f"{NOTION_PAGE.prices}",
        f"Вводный урок и первая консультация — бесплатно, в /{BOT_COMMANDS.ask}",
        ],


        BOT_COMMANDS.ask: [
            "🌗 Ты можешь задать вопрос мне лично",
            "👋 Или связаться со мной для первой консультации:",
            "@damir\\_teacher",
        ],

         BOT_COMMANDS.about: [
            "⭐ «EXPAND» — это мой авторский курс и обучение программированию.\n"
            "Ко мне приходят люди, которые хотят научиться писать код и зарабатывать в IT", 
            
            "⭐ Я могу научиться тебя HTML / CSS, JavaScript (Vue и React), Python, PHP и развить в тебе навыки фронтенд и бекенд-разработчика.",

            "⭐ Я лично готовлю все материалы, видео, задачи и проекты — и стараюсь делать их с изюминкой",

            "⭐ Ты можешь начать обучение прямо сейчас, за это не нужно платить деньги:",
            f"{NOTION_PAGE.start}",
        ], 
        
        BOT_COMMANDS.languages: "Выбери язык / обери мову", 
    }
)
