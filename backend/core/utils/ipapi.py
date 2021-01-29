import httpx

from typing import Optional


class IPApiWrapper:
    @classmethod
    async def _get_link(cls, user_ip: str) -> str:
        return f"https://ipapi.co/{user_ip}/json/"

    @classmethod
    async def get_location(cls, user_ip) -> Optional[dict]:
        link = await cls._get_link(user_ip)
        async with httpx.AsyncClient() as client:
            try:
                req = (await client.get(link)).json()
            except Exception:
                return None
            return req
