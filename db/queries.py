"""Legacy PR7 named SQL catalog; PR9 web views must not import it."""
import re
from contextlib import closing
from functools import lru_cache
from . import database

SQL_PATH = database.ROOT_DIR / 'sql' / 'queries.sql'
QUERY_MARKER = re.compile(r'^-- name: ([a-z][a-z0-9_]*)\s*$', re.MULTILINE)


@lru_cache(maxsize=1)
def catalog():
    text = SQL_PATH.read_text(encoding='utf-8')
    parts = QUERY_MARKER.split(text)
    queries = {}
    for name, statement in zip(parts[1::2], parts[2::2]):
        queries[name] = statement.strip().removesuffix(';').strip()
    if len(queries) < 10:
        raise ValueError('В sql/queries.sql должно быть не менее десяти запросов')
    return queries


def rows(name, params=()):
    with closing(database.get_connection()) as connection:
        return connection.execute(catalog()[name], params).fetchall()


def one(name, params=()):
    with closing(database.get_connection()) as connection:
        return connection.execute(catalog()[name], params).fetchone()
