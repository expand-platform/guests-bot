from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


from bot_engine.utils.Logger import Logger
from bot_engine.languages.Languages import Language

from bot_engine.bot.Bot import Bot
from bot_engine.database.Database import Database

from bot_engine.database.MongoDB import MongoDB

# consts
SCHEDULE_DAYS = [
    {"id": 0, "name": "Понедельник", "lessons": ""},
    {"id": 1, "name": "Вторник", "lessons": ""},
    {"id": 2, "name": "Среда", "lessons": ""},
    {"id": 3, "name": "Четверг", "lessons": ""},
    {"id": 4, "name": "Пятница", "lessons": ""},
    {"id": 5, "name": "Суббота", "lessons": ""},
    {"id": 6, "name": "Воскресенье", "lessons": ""},
]

class Schedule:
    def __init__(self):
        self.log = Logger().info
        
        self.scheduler = BackgroundScheduler()
        
        self.bot = Bot()
        self.messages = Language().messages
        
        self.database = self.database
        
        
    def set_scheduled_tasks(self):
        self.set_weekly_tasks()
        self.set_monthly_tasks()
        
        self.scheduler.start()
        
        
        
    def set_weekly_tasks(self):
        self.scheduler.add_job(self.make_weekly_backup, CronTrigger(day_of_week='mon', hour=10, minute=0))
        self.log(f"Weekly tasks set! 🆗")
        

    def set_monthly_tasks(self):
        self.scheduler.add_job(self.make_monthly_data_refresh, 'cron', day='last', hour=10, minute=0)
        self.log(f"Monthly tasks set! 🆗")

    
    def get_current_time(self) -> str:
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print("Formatted date and time:", formatted_datetime)
        
        return formatted_datetime
        
        
    def make_monthly_data_refresh(self):
        self.bot.tell_admins(messages=self.messages["monthly_data_refresh"]["intro"])
        
        # updates user under the hood
        # ? no need to do "sync-cache-remote"
        self.database.make_monthly_reset()
            
        self.log(f"Monthly reset completed 🤙")
        self.bot.tell_admins(messages=self.messages["monthly_data_refresh"]["success"])
            
        
    def make_weekly_backup(self):
        self.bot.tell_admins(messages=self.messages["weekly_replica"]["intro"])
        
        # replicate all collections
        MongoDB().replicate_collection(collection_name="users")
        MongoDB().replicate_collection(collection_name="versions")
        
        self.bot.tell_admins(messages=self.messages["weekly_replica"]["success"])
        
    
    #! Вынести в класс Schedule
    def week_of_month(self, dt):
        first_day = dt.replace(day=1)
        date_of_month = dt.day
        adjusted_dom = date_of_month + first_day.weekday()  # Weekday ranges from 0 (Monday) to 6 (Sunday)
        return (adjusted_dom - 1) // 7 + 1
    

    #! Вынести в класс Schedule
    # def make_monthly_reset(self):
    #     users = self.get_users()
        
    #     for user in users:
    #         #? reset lessons
    #         if user["access_level"] == "student":
    #             self.update_user(user=user, key="done_lessons", new_value=0)
    #             self.update_user(user=user, key="lessons_left", new_value=user["max_lessons"])
    #             self.update_user(user=user, key="payment_status", new_value=False)
            
    #     print(f"Monthly reset completed 🤙")

        
        

class ScheduleDays:
    def __init__(self, schedule_collection: Collection):
        self.schedule_collection = schedule_collection
        self.days = list(schedule_collection.find({}))
        # print("🐍 self.days", self.days)

    def get_days(self):
        return list(self.schedule_collection.find({}))
    
    #? get scheduled lessons from a specific day
    def get_schedule(self, day_id: int) -> str: 
        day = self.schedule_collection.find_one(filter={"id": day_id})
        print("🐍 day info (mongo): ",day)
        return day["lessons"] 

    def check_days_integrity(self):
        if len(self.days) < 7:
            print("Не все дни в порядке...")
            self.create_days()
        else: print("Все 7 дней расписания на месте!")

    #! depends on SCHEDULE_DAYS
    # def create_days(self):
    #     for day in SCHEDULE_DAYS:
    #         self.schedule_collection.insert_one(day)
    #         print(f"day {day} created in schedule!")
    
    #! depends on SCHEDULE_DAYS
    # def change_day_schedule(self, day_id: int, new_schedule: str):
    #     self.schedule_collection.update_one(filter={"id": day_id}, update={"$set": {"lessons": new_schedule} })
    #     print(f"Schedule for { SCHEDULE_DAYS[day_id]["name"]} successfully changed! ")

    def create_schedule_messages(self):
        days = self.get_days()
        messages = []

        for day in days:
            # print(f"day: {day}")
            if day["lessons"] != "":
                messages.append(day["lessons"])
            
            print("🐍 messages: ",messages)
        
        return messages
    
    def clear_schedule(self):
        self.schedule_collection.update_many({}, {"$set": {"lessons": ""}})
        print("Schedule cleared!")
