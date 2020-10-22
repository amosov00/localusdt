from fastapi import APIRouter, Depends, Path, Body, HTTPException
from typing import List, Optional
from http import HTTPStatus
from decimal import Decimal

from api.dependencies import user_is_staff_or_superuser, user_is_superuser
from database.crud import (
    USDTTransactionCRUD,
    EthereumWalletCRUD,
    ReferralCRUD,
    AdsCRUD,
    UserCRUD,
    InvoiceCRUD,
    LogCRUD
)
from core.integrations.crypto import USDTWrapper
from schemas.ads import AdsInSearch, AdsStatuses
from schemas.base import ObjectId
from schemas.logging import Log, LogInDB, LogEvents
from schemas.ethereum_wallet import EthereumWallet, EthereumWalletResponse, ServiceEthereumWalletsResponse
from schemas.invoice import InvoiceStatus, InvoiceWithAds, InvoiceInDB
from schemas.transaction import USDTTransaction, USDTTransactionStatus, USDTTransactionEvents
from schemas import User, UserUpdateNotSafe, UserTransaction
from schemas.referral import ReferralGeneralInfo
from schemas.admin_stats import DepositStatistic

__all__ = ["router"]

router = APIRouter()


@router.get("/invoices/{status}/", response_model=Optional[List[InvoiceInDB]])
async def get_all_invoices(
    user: User = Depends(user_is_staff_or_superuser),
    status: str = Path(
        ..., description="possible: 'active', 'not_active', 'under_consideration'"
    ),
):
    if status == "active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.ACTIVE)
    elif status == "not_active":
        return await InvoiceCRUD.get_invoice_by_status(status=InvoiceStatus.NOT_ACTIVE)
    elif status == "under_consideration":
        return await InvoiceCRUD.get_invoice_by_status(
            status=InvoiceStatus.FROZEN
        )


@router.get("/invoice/{invoice_id}/", response_model=InvoiceWithAds)
async def get_all_invoices(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.get_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/cancel/")
async def cancel_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.cancel_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/confirm/")
async def confirm_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.approve_invoice(user, invoice_id)


@router.put("/invoice/{invoice_id}/transfer/")
async def transfer_not_safe(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.transfer_tokens(user, invoice_id)


@router.put("/invoice/{invoice_id}/rollback/")
async def rollback_invoice(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.rollback(invoice_id)


@router.put("/invoice/{invoice_id}/freeze/")
async def freeze_invoice(
    user: User = Depends(user_is_staff_or_superuser), invoice_id: str = Path(...)
):
    return await InvoiceCRUD.freeze_invoice(invoice_id)


@router.get("/users/", response_model=Optional[List[User]], response_model_exclude={"password"})
async def get_all_users(
    user: User = Depends(user_is_staff_or_superuser)
):
    users = await UserCRUD.find_many({})
    for user in users:
        print(user)
        user["_id"] = str(user["_id"])
    return users


@router.put("/users/{user_id}/", response_model=User)
async def update_user(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: str = Path(...),
    payload: UserUpdateNotSafe = Body(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)},
        payload=payload.dict(exclude_none=True, exclude_unset=True)
    )
    user = await UserCRUD.find_by_id(user_id)
    return user


@router.get("/users/transactions/{user_id}/", response_model=List[UserTransaction])
async def get_user_transactions(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: str = Path(...)
):
    user = await UserCRUD.find_by_id(user_id)
    if not user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad user id")
    user = User(**user)
    return await UserCRUD.get_transactions(user)


@router.get("/users/info/{user_id}", response_model=User)
async def get_user_info(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: str = Path(...)
):
    return await UserCRUD.find_by_id(user_id)


@router.get("/users/referral_info/{user_id}", response_model=ReferralGeneralInfo)
async def get_user_referral_info(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: str = Path(...)
):
    user = await UserCRUD.find_by_id(user_id)
    if not user:
        raise HTTPException(HTTPStatus.BAD_REQUEST, "Bad user id")
    user = User(**user)
    return await ReferralCRUD.get_general_info(user)


@router.put("/users/ban/{user_id}/")
async def ban_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    # TODO: delete all ads and invoice for current user
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"banned": True}
    )
    return True


@router.put("/users/unban/{user_id}/")
async def unban_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"banned": False}
    )
    return True


@router.put("/users/deactivate/{user_id}/")
async def deactivate_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"is_active": False}
    )
    return True


@router.put("/users/activate/{user_id}/")
async def activate_user(
    user: User = Depends(user_is_staff_or_superuser), user_id: str = Path(...)
):
    await UserCRUD.update_one(
        query={"_id": ObjectId(user_id)}, payload={"is_active": True}
    )
    return True


@router.get("/logs/", response_model=List[Log])
async def get_logs(
    user: User = Depends(user_is_staff_or_superuser),
    event: Optional[str] = None,
    user_id: Optional[str] = None,
    invoice_id: Optional[str] = None,
    ads_id: Optional[str] = None,
    tx_hash: Optional[str] = None,
):
    log_filter = Log(
        event=event,
        user_id=ObjectId(user_id) if user_id else None,
        invoice_id=ObjectId(invoice_id) if invoice_id else None,
        ads_id=ObjectId(ads_id) if ads_id else None,
        tx_hash=tx_hash
    )
    return await LogCRUD.find_many(query=log_filter.dict(exclude_unset=True, exclude_none=True))


@router.get("/transactions/", response_model=List[USDTTransaction])
async def get_transactions(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: Optional[str] = None,
    to_adr: Optional[str] = None,
    from_adr: Optional[str] = None,
    status: Optional[USDTTransactionStatus] = None,
    event: Optional[USDTTransactionEvents] = None,
):
    tx_filter = USDTTransaction(
        user_id=ObjectId(user_id) if user_id else None,
        to_adr=to_adr,
        from_adr=from_adr,
        status=status,
        event=event
    )
    return await USDTTransactionCRUD.find_many(query=tx_filter.dict(exclude_unset=True, exclude_none=True))


@router.get("/wallets/", response_model=List[EthereumWalletResponse])
async def get_wallets(
    user: User = Depends(user_is_staff_or_superuser),
    user_email: Optional[str] = None
):
    wallets = await EthereumWalletCRUD.find_many({})
    eth_wallet_kw = {}
    for wallet in wallets:
        eth_wallet_kw[wallet.get("eth_address").lower()] = wallet
    query = User(email=user_email)
    users = await UserCRUD.find_many(query=query.dict(exclude_unset=True, exclude_none=True))
    response = []
    for user in users:
        wallet = eth_wallet_kw.get(user.get("eth_address").lower() if user.get("eth_address") else None)
        response.append({
            "email": user.get("email"),
            "eth_address": user.get("eth_address"),
            "contract_balance": wallet.get("contract_balance") if wallet else None
        })
    return response


@router.get("/service_wallets/", response_model=ServiceEthereumWalletsResponse)
async def get_service_wallets(
    user: User = Depends(user_is_staff_or_superuser),
    username: Optional[str] = None
):
    query = User(username=username)
    users = await UserCRUD.find_many(query=query.dict(exclude_unset=True, exclude_none=True))
    total: float = 0.
    response = []
    for user in users:
        service_balance = (user.get("balance_usdt") if user.get("balance_usdt") else 0.) \
            + (user.get("usdt_in_invoices") if user.get("usdt_in_invoices") else 0.)
        response.append({
            "username": user.get("username"),
            "service_balance": service_balance,
            "email": user.get("email"),
            "eth_address": user.get("eth_address"),
        })
        total += service_balance
    return {
        "total": total,
        "wallets": response
    }


@router.get("/wallets/statistic/", response_model=DepositStatistic)
async def get_stats(
    user: User = Depends(user_is_staff_or_superuser)
):
    wallets = await EthereumWalletCRUD.find_many({})
    transactions = await USDTTransactionCRUD.find_many({})
    total_deposits = Decimal(0)
    total_withdraw_pending = Decimal(0)
    total_withdraw_done = Decimal(0)
    total_on_wallets = Decimal(0)
    total_on_hot_wallet = await USDTWrapper().get_hot_wallet_balance()
    for wallet in wallets:
        total_on_wallets += wallet.get("contract_balance").to_decimal()
    for transaction in transactions:
        if transaction.get("event") == USDTTransactionEvents.WITHDRAW:
            total_withdraw_pending += transaction.get("usdt_amount").to_decimal() if transaction.get("status") == USDTTransactionStatus.PENDING else Decimal(0)
            total_withdraw_done += transaction.get("usdt_amount").to_decimal() if transaction.get("status") == USDTTransactionStatus.DONE else Decimal(0)
        elif transaction.get("event") == USDTTransactionEvents.DEPOSIT:
            total_deposits += transaction.get("usdt_amount").to_decimal() if transaction.get("status") == USDTTransactionStatus.DONE else Decimal(0)

    return {
        "total_withdraw_pending": total_withdraw_pending,
        "total_withdraw_done": total_withdraw_done,
        "total_withdraw": total_withdraw_pending + total_withdraw_done,
        "total_on_wallets": total_on_wallets,
        "total_on_hot_wallet": total_on_hot_wallet,
        "total_active": total_on_wallets + total_on_hot_wallet,
        "total": total_on_wallets + total_on_hot_wallet - total_withdraw_pending - total_withdraw_done
    }


@router.get("/orders/", response_model=List[Optional[AdsInSearch]])
async def get_orders(
    user: User = Depends(user_is_staff_or_superuser),
    username: Optional[str] = None
):
    user = await UserCRUD.find_by_username(username) if username else None
    if user:
        adses = await AdsCRUD.find_many(query={"user_id": user.get("_id")})
    else:
        adses = await AdsCRUD.find_many({})
    users = await UserCRUD.find_many(query={})
    users_kw = {}
    for user in users:
        if user.get("username"):
            users_kw[user["_id"]] = user["username"]
    for ads in adses:
        ads["username"] = users_kw[ads["user_id"]]
    return adses
