from dataclasses import dataclass, field

@dataclass
class APIClient:
    Binance: str = "Binance"

API_CLIENTS = APIClient()