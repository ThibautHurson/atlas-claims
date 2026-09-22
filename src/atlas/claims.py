"""Reading claims.

Every read is scoped to one account. An insurer sees the claims filed against
its own policies and nothing else.
"""

from atlas.db import fetchall, fetchone
from atlas.models import Claim

_COLUMNS = "id, account_id, policy_number, date_of_loss, peril, reserve_cents, status"


def list_claims(account_id: str) -> list[Claim]:
    """Every claim belonging to this account, newest loss first."""
    rows = fetchall(
        f"SELECT {_COLUMNS} FROM claims WHERE account_id = %s ORDER BY date_of_loss DESC",
        (account_id,),
    )
    return [Claim(**row) for row in rows]


def get_claim(claim_id: str, account_id: str) -> Claim | None:
    """One claim, if it belongs to this account."""
    row = fetchone(
        f"SELECT {_COLUMNS} FROM claims WHERE id = %s AND account_id = %s",
        (claim_id, account_id),
    )
    return Claim(**row) if row else None
