from dataclasses import dataclass

#! dont change this to Enum because of telebot types compatibility 
#! (gives type error str != Enum)
@dataclass
class ParseMode:
    MARKDOWN: str = "Markdown"
    MARKDOWNV2: str = "MarkdownV2"
    HTML: str = "HTML"