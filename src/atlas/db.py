"""The database connection, and the two helpers every query goes through.

Nothing in Atlas builds SQL by formatting a string: parameters are bound, so
a policy number out of a URL cannot become part of the statement.
"""

import os
from typing import Any

import psycopg
from psycopg.rows import dict_row

_connection: psycopg.Connection | None = None


def connection() -> psycopg.Connection:
    global _connection
    if _connection is None or _connection.closed:
        _connection = psycopg.connect(os.environ["ATLAS_DATABASE_URL"], row_factory=dict_row)
    return _connection


def fetchone(sql: str, params: tuple[Any, ...] = ()) -> dict[str, Any] | None:
    with connection().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchone()


def fetchall(sql: str, params: tuple[Any, ...] = ()) -> list[dict[str, Any]]:
    with connection().cursor() as cur:
        cur.execute(sql, params)
        return cur.fetchall()
