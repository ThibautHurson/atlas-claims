"""Who is asking.

The portal signs in against the identity provider and sets a session cookie.
Here we only turn that cookie back into an account.
"""

from fastapi import Cookie, HTTPException

from atlas.db import fetchone
from atlas.models import Account


def current_account(atlas_session: str | None = Cookie(default=None)) -> Account:
    """The signed-in insurer, or 401."""
    if not atlas_session:
        raise HTTPException(status_code=401, detail="Not signed in")
    row = fetchone(
        "SELECT a.id, a.name FROM sessions s JOIN accounts a ON a.id = s.account_id "
        "WHERE s.token = %s AND s.expires_at > now()",
        (atlas_session,),
    )
    if row is None:
        raise HTTPException(status_code=401, detail="Session expired")
    return Account(**row)
