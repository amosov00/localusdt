import httpx
from typing import Optional


class Currency:
    def __init__(self):
        self.rub_api_link: str = "https://api.binance.com/api/v3"
        self.rub_rate_method: str = "/ticker/24hr?symbol=USDTRUB"
        self.byn_api_link: str = "https://www.nbrb.by/api"
        self.byn_rate_method: str = "/exrates/rates/145"

    async def get_tether_rate_rub(self) -> Optional[float]:
        async with httpx.AsyncClient() as client:
            try:
                binance_req = (
                    await client.get(self.rub_api_link + self.rub_rate_method)
                ).json()
            except Exception:
                return None
        return (
            float(binance_req.get("weightedAvgPrice"))
            if binance_req.get("weightedAvgPrice")
            else None
        )

    async def get_tether_rate_byn(self) -> Optional[float]:
        async with httpx.AsyncClient() as client:
            try:
                nbrb_req = (
                    await client.get(self.byn_api_link + self.byn_rate_method)
                ).json()
            except Exception:
                return None
        return (
            float(nbrb_req.get("Cur_OfficialRate"))
            if nbrb_req.get("Cur_OfficialRate")
            else None
        )
