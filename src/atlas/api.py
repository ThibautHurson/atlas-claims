"""The HTTP routes.

`current_account` resolves the session cookie to the signed-in insurer. Every
handler passes that account down, so the query itself is what enforces who
may read what.
"""

from fastapi import Depends, FastAPI, HTTPException

from atlas import claims, invoices
from atlas.models import Account
from atlas.session import current_account

app = FastAPI(title="Atlas Claims")


@app.get("/claims")
def read_claims(status: str | None = None, account: Account = Depends(current_account)):
    if status is not None and status not in claims.STATUSES:
        raise HTTPException(status_code=400, detail=f"Unknown status {status!r}")
    return claims.list_claims(account.id, status)


@app.get("/claims/{claim_id}")
def read_claim(claim_id: str, account: Account = Depends(current_account)):
    claim = claims.get_claim(claim_id, account.id)
    if claim is None:
        raise HTTPException(status_code=404, detail="No such claim")
    return claim


@app.get("/invoices")
def read_invoices(account: Account = Depends(current_account)):
    return invoices.list_invoices(account.id)


@app.get("/invoices/{invoice_id}")
def read_invoice(invoice_id: str, account: Account = Depends(current_account)):
    invoice = invoices.get_invoice(invoice_id, account.id)
    if invoice is None:
        raise HTTPException(status_code=404, detail="No such invoice")
    return invoice
