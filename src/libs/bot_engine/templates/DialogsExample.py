class AdminDialogs:
    def __init__(self):
        self.log = Logger().info
        
        self.bot = Bot()
        
        self.dialog_generator = DialogGenerator()
        self.messages = Language().messages
        
    
    def set_admin_dialogs(self):
        #? /nv 
        #? new_version (step 1) -> prompt for version number 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="nv",
            
            active_state=None,
            next_state=VersionSequenceStates.stages[0],
            
            formatted_messages=[self.messages["prompt_new_version_number"], self.messages["latest_version"]],
            formatted_variables=["user.real_name", "latest_version"],
        )
        
        #? new_version -> (step 2) -> prompt for version message 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="state",
            
            active_state=VersionSequenceStates.stages[0],
            next_state=VersionSequenceStates.stages[1],
            state_variable="version_number",
            
            bot_before_message=self.messages["prompt_new_version_changelog"],
        )
        
        #? new_version -> (step 3) -> final (save to DB) 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="state",
            
            active_state=VersionSequenceStates.stages[1],
            next_state=None,
            state_variable="version_changelog",
            
            use_state_data=True,
            requested_state_data="new_version",
            
            database_method_name="update_version",
            database_activation_position="after_messages",
            
            bot_after_message=self.messages["new_version_success"]
        )
        
        
        #? /uu  
        #? /uu (step 1) -> update user
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="uu",
            handler_prefix="uu",
            
            active_state=None,
            next_state=UpdateUserSequenceStates.stages[0],
            
            bot_before_message=self.messages["select_user"],
            
            buttons_callback_prefix="user_id",
            keyboard_with_before_message="select_users",
        )
        
        #? /uu (step 2) -> property selection from user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="uu",
            handler_property="user_id",
            
            active_state=UpdateUserSequenceStates.stages[0],
            next_state=UpdateUserSequenceStates.stages[1],
            state_variable="user_id",
            
            bot_before_message=self.messages["select_property"],
            
            buttons_callback_prefix="user_property",
            keyboard_with_before_message="select_user_property",
        )
        
        #? /uu (step 3) -> new_value prompt for user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="uu",
            handler_property="user_property",
            
            active_state=UpdateUserSequenceStates.stages[1],
            next_state=UpdateUserSequenceStates.stages[2],
            state_variable="user_property",
            
            bot_before_message=self.messages["new_value_prompt"],
        )
        
        #? /uu (final: step 4) -> success message 
        self.dialog_generator.make_dialog(
            handler_type="state",
            handler_prefix="uu",

            active_state=UpdateUserSequenceStates.stages[2],
            next_state=None,
            state_variable="new_value",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            database_activation_position="before_messages",
            database_method_name="update_user",
            
            bot_after_message=self.messages["update_user_success"]
        )
        
        
        #? /su (see user) 
        #? /su (step 1) -> user selection 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="command",
            command_name="su",
            
            handler_prefix="su",
            buttons_callback_prefix="user_id",
            
            active_state=None,
            next_state=SeeUserSequenceStates.stages[0],
            
            bot_before_message=self.messages["su_intro"],
            keyboard_with_before_message="select_users",
        )
        
        #? /su (final: step 2) -> show user info 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
                        
            handler_prefix="su",
            handler_property="user_id",
            
            active_state=SeeUserSequenceStates.stages[0],
            next_state=None,
            state_variable="user_id",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            database_method_name="show_user",
            database_activation_position="before_messages",
            
            bot_before_message=self.messages["su_another_user"],
        )
        
        #? /be -> bulk editor
        #? step 1: select user type by access_level
        self.dialog_generator.make_dialog(
            handler_type="command",
            command_name="be",
            access_level=["admin"],
            
            active_state=None,
            next_state=BulkEditorStates.stages[0],
            
            bot_before_message=self.messages["bulk_editor"]["select_user_type"],
            
            handler_prefix="be",
            buttons_callback_prefix="access_level",
            keyboard_with_before_message="users.access_level",
        )
        
        #? /be (step 2) -> property selection from user 
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="be",
            handler_property="access_level",
            
            active_state=BulkEditorStates.stages[0],
            next_state=BulkEditorStates.stages[1],
            
            state_variable="user.category",
            use_state_data=True,
            requested_state_data="user.category",
            
            bot_before_message=self.messages["bulk_editor"]["select_user_property"],
            
            buttons_callback_prefix="user_property",
            keyboard_with_before_message="users.access_level.properties",
        )
        
        #? /be (step 3) -> new_value prompt
        self.dialog_generator.make_dialog(
            access_level=["admin"],
            handler_type="keyboard",
            handler_prefix="be",
            handler_property="user_property",
            
            active_state=BulkEditorStates.stages[1],
            next_state=BulkEditorStates.stages[2],
            state_variable="user_property",
            
            bot_before_message=self.messages["bulk_editor"]["enter_new_value"],
        )
        
        #? /be (final: step 4) -> success message 
        self.dialog_generator.make_dialog(
            handler_type="state",
            handler_prefix="be",

            active_state=BulkEditorStates.stages[2],
            next_state=None,
            state_variable="new_value",
            
            use_state_data=True,
            requested_state_data="all",
            
            database_activation_position="before_messages",
            database_method_name="bulk_update",
            
            bot_after_message=self.messages["bulk_editor"]["success"],
        )

        #! /ru remove user

        #? /ru (1): prompt for user_id
        self.dialog_generator.make_dialog(
            handler_type="command",
            command_name="ru",
            access_level=["admin"],
            
            active_state=None,
            next_state=RemoveUserStates.stages[0],
            
            bot_before_message=self.messages["remove_user"]["select_user"],
            
            handler_prefix="ru",
            buttons_callback_prefix="user_id",

            keyboard_with_before_message="select_users"
        )

        #? /ru (2) -> final: success message 
        self.dialog_generator.make_dialog(
            handler_type="keyboard",
            access_level=["admin"],
                        
            handler_prefix="ru",
            handler_property="user_id",
            
            active_state=RemoveUserStates.stages[0],
            next_state=None,
            state_variable="user_id",
            
            use_state_data=True,
            requested_state_data="selected_user",
            
            database_method_name="remove_user",
            database_activation_position="before_messages",
            
            bot_before_message=self.messages["remove_user"]["success"],
        )

        #? update_schedule (/us) (1): select day by id (inline buttons)
        self.dialog_generator.make_dialog(
            handler_type="command",
            command_name="us",
            access_level=["admin"],
            
            active_state=None,
            next_state=AdminScheduleStates.stages[0],
            
            bot_before_message=self.messages["schedule_admin"]["days_list"],

            handler_prefix="us",
            buttons_callback_prefix="day_id",

            keyboard_with_before_message="schedule.days_list"
        )

        #! not update -- get day schedule (by id) and print it out!

        #? update_schedule (/us) (2): bot sends day schedule and waits for prompt (new schedule) 
        self.dialog_generator.make_dialog(
            handler_type="keyboard",
            access_level=["admin"],
                        
            handler_prefix="us",
            handler_property="day_id",
            
            active_state=AdminScheduleStates.stages[1],
            next_state=AdminScheduleStates.stages[2],
            state_variable="schedule.day_id",
            
            #! На этом этапе не должно быть очистки state - он нужен на следующем
            use_state_data=True,
            requested_state_data="schedule.day_id",
            
            bot_before_message=self.messages["schedule_admin"]["show_day_schedule"],

            database_method_name="schedule.show_day_schedule",
            database_activation_position="after_messages",
        )
        
        #? update_schedule (/us) (3): bot sends day schedule and waits for prompt (new schedule) 
        self.dialog_generator.make_dialog(
            handler_type="state",
            access_level=["admin"],
                        
            handler_prefix="us",
            # handler_property="day_id",
            
            active_state=AdminScheduleStates.stages[2],
            next_state=None,
            state_variable="schedule.new_schedule",
            
            use_state_data=True,
            requested_state_data="schedule.all",
            
            database_method_name="schedule.update_schedule",
            database_activation_position="after_messages",
            
            bot_before_message=self.messages["schedule_admin"]["success_schedule_update"],
        )

        
        
        self.log(f"Команды / диалоги админа установлены 🥂")

    
        
        
                
            
        
        