import asyncio
from threading import Thread
from dataclasses import dataclass, field

import uvicorn
from fastapi import FastAPI
from contextlib import asynccontextmanager
from keyboard import add_hotkey

#? bot engine
from config.env import ENVIRONMENT
from libs.bot_engine.bot.Bot import Bot


@dataclass
class FastAPIServer:
    
    _app: FastAPI = field(init=False)
    _hotkey_listener_thread: Thread = field(init=False)
    _uvicorn_server: uvicorn.Server = field(init=False)

    _is_shutting_down: bool = field(default=False, init=False)


    def __post_init__(self):
        self._app = FastAPI(lifespan=self._lifespan)


    #? server run logic
    @asynccontextmanager
    async def _lifespan(self, app: FastAPI):
        print("⚡ FastAPI server started.")
        self.start_threads()
        try:
            yield
        finally:
            self.shutdown()


    def start_threads(self):
        if ENVIRONMENT in {"development", "testing"}:
            self._start_ctrl_c_listener()
        self.run_server_components()


    #? custom plug-ins
    def run_server_components(self):
        """ 
            Define your custom logic here.

            For example, you can start a bot thread here:
            
            self.bot_thread = Thread(target=self.Bot.start, name="BotThread", daemon=True)
            self.bot_thread.start()
        """
        pass


    def stop_server_components(self):
        """ 
            Define your custom components stop logic here.

            For example, you can disconnect your bot:

            self.bot.disconnect()
            
            if self._bot_thread and self._bot_thread.is_alive():
                self._bot_thread.join()
        """
        pass


    
    #? ctrl-c handling
    def _start_ctrl_c_listener(self):
        self._hotkey_listener_thread = Thread(target=self._handle_ctrl_c, name="HotkeyListener")
        self._hotkey_listener_thread.start()


    def _handle_ctrl_c(self):
        add_hotkey("ctrl+c", self.shutdown)


    #? run and stop server
    def run(self, host="127.0.0.1", port=8000):
        config = uvicorn.Config(self._app, host=host, port=port)
        self._uvicorn_server = uvicorn.Server(config)
        try:
            asyncio.run(self._uvicorn_server.serve())
        except KeyboardInterrupt:
            print("👋 Shutdown complete (graceful KeyboardInterrupt).")


    def shutdown(self):
        if self._is_shutting_down:
            return
        self._is_shutting_down = True

        print("🛑 Shutting down...")
        self.stop_server_components()

        if hasattr(self, "_uvicorn_server"):
            self._uvicorn_server.should_exit = True

        if self._hotkey_listener_thread and self._hotkey_listener_thread.is_alive():
            self._hotkey_listener_thread.join()

        print("❌ FastAPI server stopped.")
