# Atlas Claims

A small service behind the claims portal. Insurers log in, see the claims
filed against their policies, and download the invoice we bill them for.

- **Claims** — list and read the claims belonging to the signed-in account
- **Invoices** — one per account per month, priced on claims processed

## Quick start

```bash
uv sync
uv run uvicorn atlas.api:app --reload
```

## Layout

| Path | What lives there |
| --- | --- |
| `src/atlas/api.py` | the HTTP routes |
| `src/atlas/claims.py` | reading claims |
| `src/atlas/invoices.py` | reading and pricing invoices |
| `src/atlas/db.py` | the connection and two query helpers |
