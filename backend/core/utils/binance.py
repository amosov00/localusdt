import httpx
from typing import Optional


class BinanceRate:
    def __init__(self):
        self.api_link: str = "https://api.binance.com/api/v3"
        self.rate_method: str = "/ticker/24hr?symbol=USDTRUB"
        self.last_rate: Optional[float] = None

    async def get_tether_rate(self) -> Optional[float]:
        async with httpx.AsyncClient() as client:
            try:
                binance_req = (
                    await client.get(self.api_link + self.rate_method)
                ).json()
            except Exception:
                return None
        return (
            float(binance_req.get("weightedAvgPrice"))
            if binance_req.get("weightedAvgPrice")
            else None
        )
