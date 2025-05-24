from calendar import c
from typing import Union
from src.users.types import UserT

from telebot.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery,
)
from telebot.states.sync.context import StateContext

from src.database.MongoDB import MongoDB
from src.utils.Logger import Logger

from src.dialogs.data.commands_list import GUEST_SLASH_COMMANDS, STUDENT_SLASH_COMMANDS

from src.bot.Bot import Bot

from src.database.Cache import Cache
from src.database.Database import Database

from src.languages.Language import Language


class DialogGenerator:
    def __init__(self):
        self.log = Logger().info
        self.bot = Bot()
        self.messages = Language().messages

   
    # ? ADMIN COMMANDS
    def make_dialog(
        self,
        access_level=["student", "admin"],
        # ? how message is going to be handled (/test, inlineKeyboard button, state step)
        handler_type: str = "state",  # command, state, keyboard
        handler_prefix: str = None,  # uu:, su:
        # ?
        handler_property: str = None,  # user_id, user_property
        buttons_callback_prefix: str = None,  # user_id, user_property
        command_name: str = None,
        # ? states
        active_state: StateContext = None,
        next_state: StateContext = None,
        # ? state data
        state_variable: str = None,
        use_state_data: bool = False,
        requested_state_data: str = None,
        # ? messages
        bot_before_message: str = None,
        bot_after_message: str = None,
        formatted_messages: list = None,
        formatted_variables: list = None,
        # ? create a keyboard
        keyboard_with_before_message: str = None,
        keyboard_with_after_message: str = None,
        # ? mongodb
        database_activation_position: str = "after_messages",
        database_method_name: str = None,
    ):

        def set_custom_command(
            message: Union[Message, CallbackQuery], state: StateContext
        ):
            # ? initial data for keyboard reply
            call_data = None
            call_id = None

            if handler_type == "keyboard":
                call_data = message.data
                call_id = message.id
                print("🐍 call_data: ", call_data)

            # ? if we're replying to keyboard
            if not hasattr(message, "chat"):
                message = message.message

            # ? initial data for other types (state, command, etc)
            state_data = {}

            keyboard: InlineKeyboardMarkup = None

            # ? initial user data
            active_user = Database().get_active_user(message)
            messages = Language().messages

            # print("🐍 active_user (step_gen): ",active_user)

            # ? Save state's data or remove it
            if next_state:
                state.set(state=next_state)

            if active_state:
                data_for_state = None

                if call_data:
                    data_for_state = call_data

                else:
                    data_for_state = message.text

                self.log(f"user's reply or selection: { data_for_state }")

                self.save_data_to_state(
                    variable_name=state_variable,
                    data_to_save=data_for_state,
                    state=state,
                )

            if use_state_data and requested_state_data:
                state_data = self.get_state_data(
                    requested_data=requested_state_data,
                    state=state,
                    # prefixes
                    handler_prefix=handler_prefix,
                )
                print("🐍 state_data: ", state_data)

            # ? DB action (before messages)
            if (
                database_activation_position == "before_messages"
                and database_method_name
            ):
                self.choose_database_method(
                    database_method_name=database_method_name,
                    message=message,
                    active_user=active_user,
                    data_from_state=state_data,
                )

            # ? set keyboard, if needed
            if keyboard_with_before_message or keyboard_with_after_message:
                self.log(
                    f"create keyboard with text: {keyboard_with_before_message or keyboard_with_after_message}"
                )

                keyboard = self.create_inline_keyboard(
                    keyboard_type=keyboard_with_before_message
                    or keyboard_with_after_message,
                    callback_user_id=call_data,
                    # prefixes
                    handler_prefix=handler_prefix,
                    buttons_prefix=buttons_callback_prefix,
                    state_data=state_data,
                )

            # ? Messages and keyboards
            if bot_before_message:
                # when keyboard, send signal for callback_query
                if handler_type == "keyboard":
                    self.bot._bot.answer_callback_query(
                        callback_query_id=call_id,
                        text="",
                    )

                self.log(f"bot answered button (sends hints)")
                self.log(f"active_user: { active_user }")

                self.bot._bot.send_message(
                    chat_id=active_user["user_id"],
                    text=bot_before_message,
                    reply_markup=keyboard or None,
                    parse_mode="Markdown",
                )

            if formatted_messages and formatted_variables:
                self.format_message(
                    messages=formatted_messages,
                    formatting_variables=formatted_variables,
                    reply_markup=keyboard or None,
                    user=active_user,
                )

            # ? MongoDB (end)
            if (
                database_activation_position == "after_messages"
                and database_method_name
            ):
                self.choose_database_method(
                    database_method_name=database_method_name,
                    message=message or call.message,
                    data_from_state=state_data,
                )

            if bot_after_message:
                # when keyboard, send signal for callback_query
                if handler_type == "keyboard":
                    self.bot._bot.answer_callback_query(
                        callback_query_id=call_id,
                        text="",
                    )

                self.bot._bot.send_message(
                    chat_id=active_user["user_id"],
                    text=bot_after_message,
                    reply_markup=keyboard or None,
                    parse_mode="Markdown",
                )

            if not next_state:
                state.delete()

        # choose type of message handler
        if handler_type == "command":
            self.bot._bot.register_message_handler(
                callback=set_custom_command,
                commands=[command_name],
                access_level=access_level,
            )

        if handler_type == "state":
            self.bot._bot.register_message_handler(
                callback=set_custom_command,
                state=active_state,
                access_level=access_level,
            )

        if handler_type == "keyboard":
            self.bot._bot.register_callback_query_handler(
                callback=set_custom_command,
                access_level=access_level,
                func=lambda call: call.data.startswith(
                    f"{handler_prefix}:{handler_property}"
                ),
            )

    # * HELPERS
    def send_action_notification(self, active_user: dict, command_name):
        # check if user is admin
        if active_user["user_id"] in Database().admin_ids:
            self.log(
                f"⚠ Admin here, don't sending notification: { active_user["real_name"] }"
            )
            return

        real_name, last_name = Database().get_real_name(active_user=active_user)
        username = active_user.get("username")

        #! Теперь нужно будет ещё и уведомлять о нажатых кнопках / вводе и т.д
        #! Пока уведомления идут только о нажатых командах

        self.bot.tell_admin(
            message=f"{ real_name } { last_name } @{ username } зашёл в раздел /{command_name} ✅"
        )
        self.log(f"{ real_name } зашёл в раздел /{command_name} ✅")

    def set_slash_commands(self, active_user):
        if active_user["access_level"] == "guest":
            self.bot._bot.set_my_commands([])
            self.bot._bot.set_my_commands(commands=GUEST_SLASH_COMMANDS)

        # if "student" or "admin"
        else:
            self.bot._bot.set_my_commands([])
            self.bot._bot.set_my_commands(commands=STUDENT_SLASH_COMMANDS)

        self.log("😎 slash commands set")

    def get_format_variable(self, variable_name: str, active_user: dict):
        match variable_name:
            case "user.real_name":
                real_name, last_name = Database().get_real_name(active_user=active_user)
                return real_name

            case "user.payment_amount":
                currency_sign = "$"

                if active_user["currency"] == "eur":
                    currency_sign = "€"

                return f"{currency_sign}{ active_user["payment_amount"] }"

            case "user.amount":
                print("🐍 user_amount", active_user["payment_amount"])
                return active_user["payment_amount"]


            case "users.paid_amount":
                users = Database().get_users()

                paid_amount = 0

                # ? collect paid / unpaid amounts
                for user in users:
                    if user["access_level"] == "student":
                        if user["payment_status"]:
                            paid_amount += user["payment_amount"]

                print("🐍 paid_amount_uah", paid_amount)
                return paid_amount

            case "users.unpaid_amount":
                users = Database().get_users()

                unpaid_amount = 0

                # ? collect paid / unpaid amounts
                for user in users:
                    if user["access_level"] == "student":
                        if not user["payment_status"]:
                            unpaid_amount += user["payment_amount"]

                print("🐍 unpaid_amoun", unpaid_amount)
                return unpaid_amount

            case "user.payment_status":
                if active_user["payment_status"]:
                    return "✅ Ты уже оплатил(а)"

                else:
                    return "👀 Ты ещё не оплатил(а)"

            case "user.lessons_left":
                return active_user["lessons_left"]

            case "user.done":
                return active_user["lessons_left"]

            case "user.hometask":
                return active_user["hometask"]

            case "latest_version":
                latest_version = MongoDB().get_latest_versions_info(versions_limit=1)
                print(
                    "🐍latest_version (get_format_variable, from MongoDB)",
                    latest_version[0]["version"],
                )
                return latest_version[0]["version"]

            case "students.count":
                count = 0
                users = Database().get_users()

                for user in users:
                    print(f"user: {user}")
                    if user["access_level"] == "student":
                        count += 1

                return count

            # case "students.dollar_amount":
            #     total_sum = 0
            #     users = Database().get_users()

            #     for user in users:
            #         print(f"user: {user}")
            #         if user["access_level"] == "student":
            #             total_sum += user["payment_amount"]

            #     # ? range 80%-100%
            #     return f"{round(total_sum * 0.8)} - {round(total_sum)}"

            case "students.uah_amount":
                total_sum = 0
                users = Database().get_users()

                for user in users:
                    print(f"user: {user}")
                    if user["access_level"] == "student":
                        total_sum += user["payment_amount"]

                # total_sum *= EXCHANGE_RATES["usd"]

                # ? range 80%-100%
                return f"{ round(total_sum * 0.8) } - { round(total_sum) }"

            case "students.average":
                total_sum = 0
                count = 0
                users = Database().get_users()

                for user in users:
                    print(f"user: {user}")
                    if user["access_level"] == "student":
                        count += 1
                        total_sum += user["payment_amount"]

                return round(total_sum / count)

            #! Добавить поддержку для кастомных юзеров, а не только для текущего
            # case "selected_user.real_name":
            #     return

    def send_formatted_message(self, message_to_format, formatting_variable, user):
        data_for_formatting = self.get_format_variable(formatting_variable, user)

        self.bot.send_message_with_variable(
            chat_id=user["user_id"],
            message=message_to_format,
            format_variable=data_for_formatting,
        )

    def format_message(
        self, messages: list, formatting_variables: list, user: dict, reply_markup=None
    ):
        # print("🐍 messages (format_message): ", messages, type(messages))
        # print("🐍 formatting_variables (format_message): ", formatting_variables)
        formatting_data = []

        for variable in formatting_variables:
            data = self.get_format_variable(variable, user)
            formatting_data.append(data)

        # self.log(f"formatting_data (format_message): { formatting_data }")

        for message, format_data in zip(messages, formatting_data):
            # self.log(f"message (format_message): { message }")
            # self.log(f"format_data (format_message): { format_data }")

            self.bot.send_message_with_variable(
                chat_id=user["user_id"],
                message=message,
                format_variable=format_data,
                reply_markup=reply_markup,
            )

        # self.log(f"format messages with no errors 🦸‍♀️")

    def choose_database_method(
        self,
        database_method_name: str,
        message: Message,
        active_user=None,
        data_from_state=None,
    ):
        match database_method_name:
            case "clean":
                Database().clean_users()
            
            case "schedule.clear":
                Database().mongoDB.ScheduleDays.clear_schedule()

            case "fill":
                Database().sync_cache_and_remote_users()

            case "replicate_users":
                MongoDB().replicate_collection(collection_name="users")

            case "load_replica":
                MongoDB().load_replica(collection_name="users")
                Database().update_cache_users()

            case "monthly_refresh":
                Database().make_monthly_reset()

            case "update_lessons":
                # self.log(f"updating_lessons...")
                messages = Language().messages

                is_report_allowed = Database().check_done_reports_limit(
                    max_lessons=active_user["max_lessons"],
                    done_lessons=active_user["done_lessons"],
                )

                # ? Сценарий #1: отчёт можно заполнить
                if is_report_allowed:
                    formatted_messages = [messages["done"], messages["lessons_left"]]
                    formatted_variables = ["user.real_name", "user.done"]

                    Database().update_lessons(message)

                    self.format_message(
                        messages=formatted_messages,
                        formatting_variables=formatted_variables,
                        user=active_user,
                    )

                # ? Сценарий #w: отчёт нельзя заполнить, лимит
                else:
                    formatted_messages = [messages["done_forbidden"]]
                    formatted_variables = ["user.real_name"]

                    self.format_message(
                        messages=formatted_messages,
                        formatting_variables=formatted_variables,
                        user=active_user,
                    )

            case "update_version":
                MongoDB().send_new_version_update(
                    version_number=data_from_state["version_number"],
                    changelog=data_from_state["version_changelog"],
                )

            case "get_latest_versions_info":
                latest_versions = MongoDB().get_latest_versions_info(versions_limit=3)
                print("🐍 latest_versions: ", latest_versions)

                prepared_version_messages = self.prepare_version_messages(
                    mongoDB_objects=latest_versions
                )
                print("🐍 prepared_version_messages: ", prepared_version_messages)

                self.bot.send_multiple_messages(
                    chat_id=message.chat.id,
                    messages=prepared_version_messages,
                    parse_mode="Markdown",
                )

            case "update_user":
                user_to_change = Cache().get_user(data_from_state["user_id"])
                self.log(f"🐍 user_to_change: {user_to_change}")

                Database().update_user(
                    user=user_to_change,
                    key=data_from_state["user_property"],
                    new_value=data_from_state["new_value"],
                )
            
            case "update_user.payment_status":
                self.log(f"state dat (2)  { data_from_state }")

                user_to_change = Cache().get_user(data_from_state["user_id"])
                self.log(f"🐍 user_to_change: {user_to_change}")

                Database().update_user(
                    user=user_to_change,
                    key="payment_status",
                    new_value=1,
                )

            case "bulk_update":
                # ? update all users of selected category
                cache_user = Cache().get_users_from_cache()
                category = self.extract_button_callback_value(
                    data_from_state["user_category"]
                )
                user_property = self.extract_button_callback_value(
                    data_from_state["user_property"]
                )
                new_value = self.extract_button_callback_value(
                    data_from_state["new_value"]
                )

                print("🐍 category (choose_database_method): ", category)
                print("🐍 user_property (choose_database_method): ", user_property)
                print("🐍 new_value (choose_database_method): ", new_value)

                for user in cache_user:
                    self.log(f"user: {user}")

                    if user["access_level"] == category:
                        Database().update_user(
                            user=user, key=user_property, new_value=new_value
                        )

                self.log(f"Bulk editor: users updated successfully 😎")

            case "show_user":
                selected_user: UserT = Cache().get_user(
                    user_id=data_from_state["user_id"]
                )
                print("🐍 selected_user: ", selected_user)

                user_info = ""
                property_count = 0

                for key, value in selected_user.items():
                    # add extra empty line between each 2 properties
                    if property_count % 2 == 0:
                        user_info += "\n"

                    self.log(f"key: {key}")
                    self.log(f"key: {value}")

                    user_info += f"`{ key }`: *{ value }*\n"
                    property_count += 1

                self.bot._bot.send_message(
                    chat_id=active_user["chat_id"],
                    text=user_info,
                    parse_mode="Markdown",
                )

            case "remove_user":
                Database().remove_user(data_from_state["user_id"])

            case "schedule.show_day_schedule":
                print("🐍 data_from_state (choose_db_method)",data_from_state)
                day_id = data_from_state["day_id"]
                print("day_id (choose_db_method)", day_id)
                #? return day schedule
                day_schedule = Database().mongoDB.ScheduleDays.get_schedule(day_id)
                print("🐍 day_schedule (text)",day_schedule)
                
                if day_schedule == "":
                    print("if")
                    self.bot._bot.send_message(
                        chat_id=message.chat.id,
                        text=self.messages["schedule_admin"]["empty_schedule"],
                        parse_mode="Markdown",
                    )
                #? if schedule exists
                else:
                    print("else")
                    self.bot._bot.send_message(
                        chat_id=message.chat.id,
                        text=day_schedule,
                        parse_mode="Markdown",
                    )

            case "schedule.update_schedule":
                #! Тут нужны обе данные из state: id и new_schedule

                print("🐍 schedule state data (choose_db_method)", data_from_state)
                day_id = data_from_state["day_id"]
                new_schedule = data_from_state["new_schedule"]
                
                Database().mongoDB.ScheduleDays.change_day_schedule(day_id, new_schedule)

            case "schedule.show_schedule":
                messages = Database().mongoDB.ScheduleDays.create_schedule_messages()

                self.bot.send_multiple_messages(
                    chat_id=message.chat.id,
                    messages=messages,
                    parse_mode="Markdown",
                )


    def save_data_to_state(
        self,
        variable_name: str,
        data_to_save=None,
        state: StateContext = None,
    ):
        match variable_name:
            # ? versions (text only)
            case "version_number":
                state.add_data(version_number=data_to_save)

            case "version_changelog":
                state.add_data(version_changelog=data_to_save)

            # ? selected user (buttons + text)
            case "user_id":
                state.add_data(id=data_to_save)

            case "user_property":
                state.add_data(user_property=data_to_save)

            case "new_value":
                state.add_data(new_value=data_to_save)

            case "user.category":
                state.add_data(user_category=data_to_save)
            
            #? schedule
            case "schedule.day_id":
                state.add_data(day_id=data_to_save)
            
            case "schedule.new_schedule":
                state.add_data(new_schedule=data_to_save)

    def get_state_data(
        self,
        requested_data: str = None,
        state: StateContext = None,
        handler_prefix: str = None,
    ):

        #! Нужно просто возвращать все данные из state, какими бы они ни были

        match requested_data:
            case "new_version":
                with state.data() as data:
                    version_number = data.get("version_number")
                    version_changelog = data.get("version_changelog")

                    return {
                        "version_number": version_number,
                        "version_changelog": version_changelog,
                    }

            case "selected_user":
                self.log(f"state.data(): { vars(state.data())["data"] }")

                state_object = {}

                with state.data() as data:
                    user_id = None
                    user_property_name = None
                    new_value = None

                    if data["id"]:
                        user_id = int(
                            data.get("id").removeprefix(f"{handler_prefix}:user_id:")
                        )
                        self.log(f"user_id (get_state_data): { user_id }")
                        state_object["user_id"] = user_id

                    if data["user_property"]:
                        user_property_name = data.get("user_property").removeprefix(
                            f"{handler_prefix}:user_property:"
                        )
                        self.log(
                            f"user_property (get_state_data): { user_property_name } -> {type(user_property_name)}"
                        )
                        state_object["user_property"] = user_property_name

                    if data["new_value"]:
                        new_value = data.get("new_value")
                        self.log(f"new_value (get_state_data): { new_value }")
                        state_object["new_value"] = self.set_correct_property_type(
                            property_name=user_property_name, value_to_correct=new_value
                        )

                return state_object

            case "user.category":
                # ? extract category from state
                with state.data() as data:
                    if data["user_category"]:
                        selected_day = data["user_category"]
                        print(
                            "🐍 selected_category: (create_inline_keyboard)",
                            selected_day,
                        )

                return {"category": selected_day}


            case "schedule.day_id":
                with state.data() as data:
                    print("🐍 data",data)
                    if data["day_id"]:
                        day_id_str = data.get("day_id").removeprefix(
                            f"{handler_prefix}:day_id:"
                        )
                        print("🐍 day_id_str",day_id_str)
                        day_id = self.set_correct_property_type(
                            property_name="day_id", value_to_correct=day_id_str
                        )
                        print("🐍 day_id",day_id)
                        
                        return {"day_id": day_id}
            
            case "schedule.all":
                state_obj = {}
                with state.data() as data:
                    print("🐍 data",data)
                    if data["day_id"]:
                        day_id_str = data.get("day_id").removeprefix(
                            f"{handler_prefix}:day_id:"
                        )
                        print("🐍 day_id_str",day_id_str)
                        day_id = self.set_correct_property_type(
                            property_name="day_id", value_to_correct=day_id_str
                        )
                        print("🐍 day_id",day_id)
                        
                        state_obj["day_id"] = day_id
                    
                    if data["new_schedule"]:
                        new_schedule_str = data.get("new_schedule").removeprefix(
                            f"{handler_prefix}:new_schedule:"
                        )

                        print("🐍 new_schedule_str",new_schedule_str)
                        new_schedule = self.set_correct_property_type(
                            property_name="new_schedule", value_to_correct=new_schedule_str
                        )
                        
                        print("🐍 new_schedule: ", new_schedule)
                        state_obj["new_schedule"] = new_schedule
                #? return all schedule data
                return state_obj
                    

            case "all":
                with state.data() as data:
                    print("🐍 state data (get_state_data): ", data)

                    return data

    def prepare_version_messages(self, mongoDB_objects: list[dict]) -> list[dict]:
        prepared_version_messages = []

        for object in mongoDB_objects:
            version_message = f"*v{ object["version"] }* ({ object["date"] })\n\n{ object["changelog"] }"
            # print("🐍 new formatted object: ", version_message)

            prepared_version_messages.append(version_message)

        return prepared_version_messages

    # * MESSAGE TYPES
    def create_inline_keyboard(
        self,
        keyboard_type: str = "select_users",  # properties etc
        row_width: int = 2,
        callback_user_id: str = None,
        handler_prefix: str = None,
        buttons_prefix: str = None,
        state_data: dict = {},
    ) -> InlineKeyboardMarkup:

        keyboard = InlineKeyboardMarkup([], row_width=row_width)
        cache_users = Cache().get_users_from_cache()

        match keyboard_type:
            case "select_users":
                for user in cache_users:
                    print("🐍user: ", user)
                    real_name, last_name = Database().get_real_name(active_user=user)
                    user_id = user["user_id"]

                    button_callback_data = (
                        f"{handler_prefix}:{buttons_prefix}:{user_id}"
                    )
                    print("🐍button_callback_data: ", button_callback_data)

                    day_button = InlineKeyboardButton(
                        text=real_name, callback_data=button_callback_data
                    )
                    keyboard.add(day_button)

            case "select_user_property":
                callback_user_id = callback_user_id.removeprefix(
                    f"{handler_prefix}:user_id:"
                )
                callback_user_id = int(callback_user_id)

                print("🐍 callback_user_id: ", callback_user_id)

                selected_user = Cache().get_user(user_id=callback_user_id)
                print("🚀 selected_user: ", selected_user)

                for user_property in selected_user:
                    print("🚀 user_property: ", user_property)
                    day_button = InlineKeyboardButton(
                        text=user_property,
                        callback_data=f"{handler_prefix}:user_property:{user_property}",
                    )
                    keyboard.add(day_button)

            case "users.payment_status":
                for user in cache_users:
                    if user["access_level"] == "student":
                        print("🐍user: ", user)

                        real_name, last_name = Database().get_real_name(
                            active_user=user
                        )
                        user_id = user["user_id"]

                        payment_status = user["payment_status"]
                        payment_sign = "❌"
                        print("🐍 payment_status", payment_status)

                        if payment_status:
                            payment_sign = "✅"

                        payment_amount = user["payment_amount"]
                        print("🐍 payment_amount", payment_amount)

                        # payment_amount_uah = payment_amount * EXCHANGE_RATES["usd"]

                        button_callback_data = (
                            f"{handler_prefix}:{buttons_prefix}:{user_id}"
                        )
                        print("🐍button_callback_data: ", button_callback_data)

                        button_text = (
                            f"{payment_sign} {real_name} {payment_amount} грн"
                        )
                        print("🐍 button_text", button_text)

                        day_button = InlineKeyboardButton(
                            text=button_text, callback_data=button_callback_data
                        )
                        keyboard.add(day_button)

            #! hometask, скорее всего, не будет
            # case "hometask_actions":
            #     for key, value in self.messages["hometask"]["buttons"].items():
            #         self.log(f"key: {key}")
            #         self.log(f"key: {value}")

            #         self.log(
            #             f"button callback data: {handler_prefix}:{buttons_prefix}:{key}"
            #         )

            #         hometask_button = InlineKeyboardButton(
            #             text=value,
            #             callback_data=f"{handler_prefix}:{buttons_prefix}:{key}",
            #         )
            #         keyboard.add(hometask_button)

            case "schedule.days_list":
                days_list = Database().mongoDB.ScheduleDays.get_days()
                print("🐍 days_list",days_list)

                for day in days_list:
                    # print(f"day: {day}")
                    day_button = InlineKeyboardButton(
                        text=day["name"],
                        callback_data=f"{handler_prefix}:{buttons_prefix}:{day["id"]}",
                    )
                    keyboard.add(day_button)
                    

            case "users.access_level":
                user_categories = set()

                for user in cache_users:
                    user_categories.add(user["access_level"])

                self.log(
                    f"🐍 unique user_categories (create_inline_keyboard):  {user_categories}"
                )

                for category in user_categories:
                    # self.log(f"unique category: {category}")

                    self.log(
                        f"button callback data: {handler_prefix}:{buttons_prefix}:{category}"
                    )

                    day_button = InlineKeyboardButton(
                        text=category,
                        callback_data=f"{handler_prefix}:{buttons_prefix}:{category}",
                    )
                    keyboard.add(day_button)

            #! Написать метод extract_state_data()
            case "users.access_level.properties":
                selected_category = self.extract_button_callback_value(
                    state_data["category"]
                )
                print(
                    "🐍 selected_category (create_inline_keyboard): ", selected_category
                )

                user_within_category = Cache().find_user_by_property(
                    property_name="access_level", value=selected_category
                )

                for user_property, value in user_within_category.items():
                    # print("🚀 property: ", key)

                    day_button = InlineKeyboardButton(
                        text=user_property,
                        callback_data=f"{handler_prefix}:{buttons_prefix}:{user_property}",
                    )
                    keyboard.add(day_button)

        return keyboard

    def set_correct_property_type(
        self, property_name: str = None, value_to_correct: Union[str, int] = None
    ):
        if property_name in [
            "max_lessons",
            "done_lessons",
            "lessons_left",
            "payment_amount",
            "day_id",
        ]:
            return int(value_to_correct)

        if property_name in [
            "real_name",
            "last_name",
            "first_name",
            "username",
            "currency",
            "new_schedule",
        ]:
            return str(value_to_correct)

        if property_name in ["payment_status"]:
            if (
                value_to_correct == "True"
                or value_to_correct == "true"
                or value_to_correct == "t"
                or value_to_correct == "1"
            ):
                return True

            if (
                value_to_correct == "False"
                or value_to_correct == "false"
                or value_to_correct == "f"
                or value_to_correct == "0"
            ):
                return False

    def extract_button_callback_value(self, callback_text):
        words_array = callback_text.split(":")
        length = len(words_array)

        self.log(f"true button value: { words_array[length - 1] }")

        return words_array[length - 1].strip()
