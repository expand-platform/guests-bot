#? classes to work with 3rd-party API's
from dataclasses import field, dataclass
from typing import Any, Optional

#? bot-specific
from binance.client import Client


@dataclass
class API:
    TOKEN: str
    SECRET: Optional[str]

    client: Any = field(init=False)
    clients: dict = field(init=False)


    def add_client(self, client_name: str, api_client: Any) -> None:
        """ method for adding multiple API client (when needed) """
        self.clients[client_name] = api_client


    def get_client(self, client_name: str) -> Any:
        """ method for getting API client by name """
        return self.clients.get(client_name, None)


@dataclass
class BinanceAPI(API):
    """ class for working with Binance API """

    def __post_init__(self):
        """ creates a client / connection to API """
        self.client: Client = Client(api_key=self.TOKEN, api_secret=self.SECRET) 


    def show_btc_price(self) -> str:
        """ returns current BTC price in USDT """
        try:
            ticker = self.client.get_symbol_ticker(symbol="BTCUSDT")
            return ticker['price']
        except Exception as e:
            return f"Error fetching BTC price: {str(e)}"
