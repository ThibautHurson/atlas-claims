"""An invoice as CSV, for finance teams who reconcile in a spreadsheet."""

import csv
import io

from atlas.models import Invoice

HEADERS = ("invoice", "period", "claims processed", "price per claim", "amount due")


def invoice_csv(invoice: Invoice, price_per_claim_cents: int) -> str:
    """One invoice as a two-line CSV: the header, then the invoice."""
    out = io.StringIO()
    writer = csv.writer(out)
    writer.writerow(HEADERS)
    writer.writerow(
        [
            invoice.id,
            invoice.period,
            invoice.claims_processed,
            f"{price_per_claim_cents / 100:.2f}",
            f"{invoice.amount_cents / 100:.2f}",
        ]
    )
    return out.getvalue()
