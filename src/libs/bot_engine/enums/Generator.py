from enum import Enum


class HandlerType(Enum):
    SLASH_COMMAND = "slash_command"
    STATE = "state"
    INLINE_KEYBOARD = "inline_keyboard"
    REPLY_KEYBOARD = "reply_keyboard"


class ActivationMoment(Enum):
    BEFORE_MESSAGE = "before_message"
    AFTER_MESSAGE = "after_message"


class SendWithMessage(Enum):
    FIRST = "first_message"
    LAST = "last_message"
