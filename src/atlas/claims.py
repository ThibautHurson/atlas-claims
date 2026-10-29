"""Reading claims.

Every read is scoped to one account. An insurer sees the claims filed against
its own policies and nothing else.
"""

from atlas.db import fetchall, fetchone
from atlas.models import Claim

_COLUMNS = "id, account_id, policy_number, date_of_loss, peril, reserve_cents, status"


#: The statuses a claim can be in. Anything else is a bad request.
STATUSES = ("open", "under-review", "settled", "declined")


#: How many claims one page of the list holds.
PAGE_SIZE = 50


def list_claims(
    account_id: str, status: str | None = None, page: int = 1
) -> tuple[list[Claim], int]:
    """One page of this account's claims, newest loss first, and the total.

    The total is what the portal draws its pager from: with `status`, it
    counts the claims in that status.
    """
    offset = (page - 1) * PAGE_SIZE
    if status is None:
        rows = fetchall(
            f"SELECT {_COLUMNS} FROM claims WHERE account_id = %s "
            "ORDER BY date_of_loss DESC LIMIT %s OFFSET %s",
            (account_id, PAGE_SIZE, offset),
        )
    else:
        rows = fetchall(
            f"SELECT {_COLUMNS} FROM claims WHERE account_id = %s AND status = %s "
            "ORDER BY date_of_loss DESC LIMIT %s OFFSET %s",
            (account_id, status, PAGE_SIZE, offset),
        )
    claims = [Claim(**row) for row in rows]
    return claims, len(claims)


def get_claim(claim_id: str, account_id: str) -> Claim | None:
    """One claim, if it belongs to this account."""
    row = fetchone(
        f"SELECT {_COLUMNS} FROM claims WHERE id = %s AND account_id = %s",
        (claim_id, account_id),
    )
    return Claim(**row) if row else None


def open_reserve_cents(account_id: str) -> int:
    """What this account currently has reserved against unsettled claims."""
    row = fetchone(
        "SELECT COALESCE(SUM(reserve_cents), 0) AS total FROM claims "
        "WHERE account_id = %s AND status IN ('open', 'under-review')",
        (account_id,),
    )
    return int(row["total"]) if row else 0
