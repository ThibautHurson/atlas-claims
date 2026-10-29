from atlas.csv_export import HEADERS, invoice_csv
from atlas.models import Invoice

INVOICE = Invoice(
    id="INV-2026-09-northwind",
    account_id="acc-northwind",
    period="2026-09",
    claims_processed=1_450,
    amount_cents=348_000,
    status="issued",
)


def test_the_header_names_what_finance_reconciles():
    assert invoice_csv(INVOICE, 240).splitlines()[0] == ",".join(HEADERS)


def test_money_is_written_in_units_not_cents():
    assert invoice_csv(INVOICE, 240).splitlines()[1].endswith("2.40,3480.00")
