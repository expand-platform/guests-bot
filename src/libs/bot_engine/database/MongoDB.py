from dataclasses import dataclass, field
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection
from pymongo.database import Database

#? bot engine
from libs.bot_engine.users.User import NewUser, User


@dataclass
class MongoDB:
    """ MongoDB driver """
    TOKEN: str
    DATABASE_NAME: str
    SUPER_ADMIN_ID: int
    MAX_CONNECTIONS: int = 1
    USER_COLLECTION: str = "users"

    _database: Database = field(init=False)
    _client: MongoClient = field(init=False)

    def __post_init__(self):
        self._client = MongoClient(self.TOKEN, maxPoolSize=self.MAX_CONNECTIONS)
        self._database = self._client[self.DATABASE_NAME]
        self.users_collection: Collection = self._database[self.USER_COLLECTION]
        self.versions_collection: Collection = self._database["versions"]
        self.schedule_collection: Collection = self._database["schedule"]
        print(f"🏗 База данных {self.DATABASE_NAME} подключена!")



    def show_users(self):
        print(f"Коллекция юзеров: {list(self.users_collection.find({}))}")


    def get_all_users(self) -> list[dict [str, Any]]:
        db_users: list[dict[str, Any]] = list(self.users_collection.find({}))

        if db_users:  
            return db_users
        
        else:
            print("🟥 No users in DB!")
            return []  



    def get_all_documents(self, collection_name="users", database_name: str | None = None) -> list[dict[str, Any]]:
        database_name = database_name or self.DATABASE_NAME 
        database = self._client[database_name]

        return list(database[collection_name].find({}))


    def check_if_user_exists(self, user_id: int):
        """returns True if user is in the collection, False - if not"""
        user = self.users_collection.find_one({"user_id": user_id})

        if user:
            return True
        else:
            return False


    #! MongoDB принимает только dict
    def add_user(self, new_user: User) -> None:
        is_user_in_db = self.check_if_user_exists(new_user.user_id)
        print("🐍 user_is_in_db",is_user_in_db)

        if not is_user_in_db:
            self.users_collection.insert_one(new_user.to_dict())
            print(f"🟢 Юзер с id { new_user.user_id } сохранён в БД")
        else: 
            print(f"🟡 Юзер с id { new_user.user_id } уже есть в БД")


    def remove_user(self, user_id: int) -> None:
        filter = {"user_id": user_id}
        self.users_collection.delete_one(filter=filter)
        print(f"User removed from MongoDB!")


    def update_user(self, user_id: int, key: str, new_value: str | int | bool):
        filter_by_id = {"user_id": user_id}
        update_operation = {"$set": {key: new_value}}

        self.users_collection.update_one(filter=filter_by_id, update=update_operation)


    # ? Admin commands
    def clean_users(self):
        delete_filter = {"user_id": {"$nin": [self.SUPER_ADMIN_ID]}}

        self.users_collection.delete_many(filter=delete_filter)
        print(f"🧹 Коллекция users очищена (все, кроме админа {self.SUPER_ADMIN_ID})!")

    