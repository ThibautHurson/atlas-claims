from atlas.invoices import PRICE_PER_CLAIM_CENTS, price


def test_an_empty_month_costs_nothing():
    assert price(0) == 0


def test_a_month_is_priced_per_claim():
    assert price(120) == 120 * PRICE_PER_CLAIM_CENTS
