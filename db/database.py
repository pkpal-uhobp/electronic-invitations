"""Legacy PR7 sqlite3 access: retained for historical tests and JSON import only."""
import sqlite3
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
DB_PATH = ROOT_DIR / 'data' / 'invitations.sqlite'
SCHEMA_PATH = ROOT_DIR / 'sql' / 'schema.sql'


def get_connection(path=None):
    actual_path = Path(path) if path is not None else DB_PATH
    connection = sqlite3.connect(actual_path)
    connection.row_factory = sqlite3.Row
    connection.execute('PRAGMA foreign_keys = ON')
    return connection


def initialize_database(connection):
    connection.executescript(SCHEMA_PATH.read_text(encoding='utf-8'))
