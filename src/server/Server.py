from dataclasses import dataclass, field
from threading import Thread

#? bot engine
from libs.bot_engine.server.FastAPIServer import FastAPIServer
from libs.bot_engine.bot.Bot import Bot


@dataclass
class BotServer(FastAPIServer):
    """ Bot server build on top of FastAPIServer """
    bot: Bot
    _bot_thread: Thread = field(init=False)


    def run_server_components(self):
        """ custom server logic for my bot server """
        self._bot_thread = Thread(target=self.bot.start, name="BotThread", daemon=True)
        self._bot_thread.start()


    def stop_server_components(self):
        """ custom stop logic for my bot server """
        self.bot.disconnect()

        if self._bot_thread and self._bot_thread.is_alive():
            self._bot_thread.join()

