import asyncio

from database.crud import UserCRUD, ReferralCRUD


async def restore_referrals():
    users = await UserCRUD.find_many({})
    for user in users:
        referral = await ReferralCRUD.find_one(query={"user_id": user.get("_id")})
        if not referral:
            await ReferralCRUD.create_referral(user_id=str(user.get("_id")), referral_id=None)

if __name__ == '__main__':
    asyncio.get_event_loop().run_until_complete(restore_referrals())
