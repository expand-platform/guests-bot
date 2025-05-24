from dataclasses import dataclass, asdict
from typing import Optional, Any

from telebot.types import Message
from datetime import datetime

# ? engine
from libs.bot_engine.languages.Languages import Languages
from libs.bot_engine.enums.User import AccessLevel, CreateMethod


@dataclass
class User:
    first_name: str
    username: str

    user_id: int
    chat_id: int

    access_level: AccessLevel

    language: str 
    joined_at: str

    def to_dict(self):
        dict = asdict(self)
        dict["access_level"] = self.access_level.value
        return dict


@dataclass
class NewUser:
    """creates user from it's message data or from database"""
    access_level: AccessLevel = AccessLevel.USER

    def create_user_from_database(self, user) -> User:
        return User(
            first_name=user["first_name"],
            username=user["username"],
            
            user_id=user["user_id"],
            chat_id=user["chat_id"],
            
            access_level=self.access_level,
            
            language="ru",
            joined_at=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        )
    

    def create_user_from_message(self, message: Message) -> User:
        """ creates user from message data"""
        return User(
            first_name=message.from_user.first_name,
            username=message.from_user.username,
            
            user_id=message.from_user.id,
            chat_id=message.chat.id,
            
            access_level=self.access_level,
            
            language="ru",
            joined_at=datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
        )
    


@dataclass
class UserProfile:
    user_message: Message

    def get_first_name(self) -> str:
        """return user first_name"""
        return self.user_message.from_user.first_name or "not set"

    def get_username(self) -> str:
        """returns user @username"""
        return self.user_message.from_user.username or "not set"
