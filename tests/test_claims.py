from datetime import date

from atlas.models import Claim


def test_a_claim_carries_its_account():
    claim = Claim(
        id="CLM-1001",
        account_id="acc-northwind",
        policy_number="PN-55012",
        date_of_loss=date(2026, 8, 14),
        peril="flood",
        reserve_cents=480_000,
        status="open",
    )
    assert claim.account_id == "acc-northwind"
    assert claim.reserve_cents == 480_000
