from typing import Union

from schemas.invoice import InvoiceInDB
from schemas.user import User


class InvoiceMechanics:
    def __init__(self, invoice: Union[dict, InvoiceInDB], user: Union[dict, User] = None):
        if isinstance(invoice, dict):
            invoice = InvoiceInDB(**invoice)

        if user and isinstance(user, dict):
            user = User(**user)

        self.invoice = invoice
        self.user = user
        self.errors = []
