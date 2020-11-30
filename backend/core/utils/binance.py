import httpx
from typing import Optional


class Currency:
    def __init__(self):
        self.binance_api_link: str = "https://api.binance.com/api/v3/ticker/24hr?symbol="
        self.binance_us_api_link: str = "https://api.binance.us/api/v3/ticker/24hr?symbol="
        self.rub_rate_symbol: str = "USDTRUB"
        self.usd_rate_symbol: str = "USDTUSD"
        self.eur_rate_symbol: str = "EURUSDT"
        self.byn_api_link: str = "https://www.nbrb.by/api"
        self.byn_rate_method: str = "/exrates/rates/145"

    async def make_request(self, link) -> Optional[dict]:
        async with httpx.AsyncClient() as client:
            try:
                req = (
                    await client.get(link)
                ).json()
            except Exception:
                return None
            return req

    async def get_tether_rate_rub(self) -> Optional[float]:
        binance_req = await self.make_request(self.binance_api_link + self.rub_rate_symbol)
        if not binance_req:
            return None

        return (
            float(binance_req.get("weightedAvgPrice"))
            if binance_req.get("weightedAvgPrice")
            else None
        )

    async def get_tether_rate_byn(self) -> Optional[float]:
        nbrb_req = await self.make_request(self.byn_api_link + self.byn_rate_method)
        if not nbrb_req:
            return None
        return (
            float(nbrb_req.get("Cur_OfficialRate"))
            if nbrb_req.get("Cur_OfficialRate")
            else None
        )

    async def get_tether_rate_eur(self) -> Optional[float]:
        binance_req = await self.make_request(self.binance_api_link + self.eur_rate_symbol)
        if not binance_req:
            return None
        return (
            (1 / float(binance_req.get("weightedAvgPrice")))
            if binance_req.get("weightedAvgPrice")
            else None
        )

    async def get_tether_rate_usd(self) -> Optional[float]:
        binance_req = await self.make_request(self.binance_us_api_link + self.usd_rate_symbol)
        if not binance_req:
            return None
        return (
            float(binance_req.get("weightedAvgPrice"))
            if binance_req.get("weightedAvgPrice")
            else None
        )