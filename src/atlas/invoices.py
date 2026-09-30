"""Reading and pricing invoices.

One invoice per account per calendar month. An invoice id is not a secret,
but it is not an authorisation either: every lookup is scoped to the account
asking for it.
"""

from atlas.db import fetchall, fetchone
from atlas.models import Invoice

_COLUMNS = "id, account_id, period, claims_processed, amount_cents, status"

#: What we charge for one processed claim, in cents.
PRICE_PER_CLAIM_CENTS = 240


def price(claims_processed: int) -> int:
    """What an account owes for a month's processing."""
    return claims_processed * PRICE_PER_CLAIM_CENTS


def list_invoices(account_id: str) -> list[Invoice]:
    """Every invoice for this account, newest period first."""
    rows = fetchall(
        f"SELECT {_COLUMNS} FROM invoices WHERE account_id = %s ORDER BY period DESC",
        (account_id,),
    )
    return [Invoice(**row) for row in rows]


def get_invoice(invoice_id: str, account_id: str) -> Invoice | None:
    """One invoice, if it belongs to this account."""
    row = fetchone(
        f"SELECT {_COLUMNS} FROM invoices WHERE id = %s AND account_id = %s",
        (invoice_id, account_id),
    )
    return Invoice(**row) if row else None
