from telebot.types import BotCommand
#? bot engine
from libs.bot_engine.languages.Locale import Locale

RU_LOCALE = Locale(
    language="ru",
    
    menu_commands=[
        BotCommand(command="start", description="Старт"),
        BotCommand(command="about", description="Два слова о платформе"),
        BotCommand(command="prices", description="Цены"),
        BotCommand(command="way", description="Направления"),

    ],

    messages=
        { 
            "start": "Привет, {}! Чудный день, не так ли?", 
            "about": "Платформа EXPAND — дом всех программистов и людей, которые любят учиться, расти и развиваться.\n\nВ рамках обучения можно пройти курс по JavaScript, Python, PHP и стать фронтенд или бекенд-разработчиком. Автор платформы, Дамир, сам лично пишет материалы, ведёт уроки, учит вас искать своё место на рынке труда и помогает с трудоустройством", 
            "prices": "*Цена обучения*\n\n*Classic*\n- Группа до 8 человек\n-Груповой план уроков\n-Доступный тариф\n-1200 грн / месяц",
            "way": "*Направления для изучения*\n\n1. Фронтенд на JavaScript\n\n2. Бекенд на Python"
        }
)
