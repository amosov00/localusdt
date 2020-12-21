from fastapi import APIRouter, Depends, Path, Body, HTTPException, Query
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
from schemas.logging import Log
from schemas.base import ObjectId
from schemas.ads import AdsInSearch
from core.integrations.crypto import USDTWrapper
from schemas.referral import ReferralGeneralInfo
from schemas.admin_stats import DepositStatistic, AccountWalletInfos
from schemas import User, UserUpdateNotSafe, UserTransaction, UserAdminView
from schemas.invoice import InvoiceStatus, InvoiceWithAds, InvoiceInAdminPanel
from schemas.ethereum_wallet import EthereumWalletResponse, ServiceEthereumWalletsResponse
from schemas.transaction import USDTTransaction, USDTTransactionStatus, USDTTransactionEvents

__all__ = ["router"]

router = APIRouter()


@router.get("/invoices/", response_model=Optional[List[InvoiceInAdminPanel]])
async def get_all_invoices(
    user: User = Depends(user_is_staff_or_superuser),
    statuses: Optional[List[str]] = Query(
        default=["all"], description="possible: 'active', 'not_active', 'under_consideration', 'all'"
    ),
):
    statuses_set = set()
    for status in statuses:
        if status == "all":
            [statuses_set.add(i) for i in InvoiceStatus.ALL]
        elif status == "active":
            [statuses_set.add(i) for i in InvoiceStatus.ACTIVE]
        elif status == "not_active":
            [statuses_set.add(i) for i in InvoiceStatus.NOT_ACTIVE]
        elif status == "under_consideration":
            statuses_set.add(InvoiceStatus.FROZEN)

    result = await InvoiceCRUD.get_invoice_by_statuses(list(statuses_set))
    users = await UserCRUD.find_many({})
    user_kw = {}

    for user in users:
        user_kw[str(user.get("_id"))] = user.get("username")

    for invoice in result:
        invoice["seller_nickname"] = user_kw.get(str(invoice.get("seller_id")))
        invoice["buyer_nickname"] = user_kw.get(str(invoice.get("buyer_id")))

    return result


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


@router.get("/users/", response_model=Optional[List[UserAdminView]], response_model_exclude={"password"})
async def get_all_users(
    user: User = Depends(user_is_staff_or_superuser),
    eth_address: str = Query(default=None)
):
    if eth_address:
        users = await UserCRUD.find_many({"eth_address": eth_address.lower()})
    else:
        users = await UserCRUD.find_many({})

    wallets = await EthereumWalletCRUD.find_many({})
    wallet_kw = {}

    for wallet in wallets:
        wallet_kw[wallet.get("eth_address").lower()] = wallet

    for user in users:
        user["_id"] = str(user["_id"])
        user["contract_balance"] = wallet_kw.get(user.get("eth_address").lower()).get("contract_balance") if user.get("eth_address") else None
        user["ethereum_balance"] = wallet_kw.get(user.get("eth_address").lower()).get("ethereum_balance") if user.get("eth_address") else None

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


@router.put("/users/status/{user_id}/{status}")
async def set_user_status(
    user: User = Depends(user_is_staff_or_superuser),
    user_id: str = Path(...),
    status: str = Path(..., description="possible: 'active', 'freezed', 'blocked")
):
    # TODO: delete all ads and invoice for current user
    if status == "freezed":
        await UserCRUD.update_one(
            query={"_id": ObjectId(user_id)}, payload={
                "banned": True,
                "is_active": True
            }
        )
    elif status == "blocked":
        await UserCRUD.update_one(
            query={"_id": ObjectId(user_id)}, payload={"is_active": False}
        )
    elif status == "active":
        await UserCRUD.update_one(
            query={"_id": ObjectId(user_id)}, payload={
                "banned": False,
                "is_active": True
            }
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


@router.get("/get_wallet_info/", response_model=AccountWalletInfos)
async def get_wallet_info(
    user: User = Depends(user_is_staff_or_superuser),
):
    users = await UserCRUD.find_many({})
    result = []
    usdt_wrapper = USDTWrapper()
    for user in users:
        wallet = await EthereumWalletCRUD.find_one({"eth_address": user.get("eth_address")})
        if wallet:
            result.append({
                "email": user.get("email"),
                "eth_address": user.get("eth_address"),
                "private_key": wallet.get("private_key"),
                "amount_usdt": Decimal(await usdt_wrapper.get_balance_contract(wallet.get("eth_address"))),
                "amount_eth": Decimal(await usdt_wrapper.get_eth_balance(wallet.get("eth_address")))
            })
    return {
        "accounts": result
    }


@router.get("/loot_ether_from_wallets/")
async def loot_ether_from_wallets(
    user: User = Depends(user_is_staff_or_superuser),
):
    await USDTWrapper().loot_eth_from_wallets()
