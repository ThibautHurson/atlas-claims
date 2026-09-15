"""The three shapes the API returns."""

from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
class Account:
    id: str
    name: str


@dataclass(frozen=True)
class Claim:
    id: str
    account_id: str
    policy_number: str
    date_of_loss: date
    peril: str
    reserve_cents: int
    status: str


@dataclass(frozen=True)
class Invoice:
    id: str
    account_id: str
    period: str
    claims_processed: int
    amount_cents: int
    status: str
