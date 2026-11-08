"""Original PR7: sync legacy JSON data to a separate SQLite database.

Only for the PR7 source database, NOT the Django ORM database.
Run: python -m db.import_json [--database PATH]
"""
import argparse
import json
from pathlib import Path
from .database import DB_PATH, ROOT_DIR, get_connection, initialize_database


def read_list(path):
    with path.open(encoding='utf-8') as source:
        data = json.load(source)
    if not isinstance(data, list):
        raise ValueError(f'Ожидается JSON-массив: {path}')
    return data


def import_json(data_dir=None, db_path=None):
    data_dir = Path(data_dir) if data_dir is not None else ROOT_DIR / 'data'
    db_path = Path(db_path) if db_path is not None else DB_PATH
    users = read_list(data_dir / 'users.json')
    guests = read_list(data_dir / 'guests.json')
    events = read_list(data_dir / 'events.json')
    invitations = read_list(data_dir / 'invitations.json')
    db_path.parent.mkdir(parents=True, exist_ok=True)
    connection = get_connection(db_path)
    try:
        initialize_database(connection)
        user_ids = {int(user['id']) for user in users}
        guest_ids = {int(guest['id']) for guest in guests}
        with connection:
            for statement in ('DELETE FROM invitations', 'DELETE FROM events',
                              'DELETE FROM guests', 'DELETE FROM users'):
                connection.execute(statement)
            connection.executemany(
                'INSERT INTO users(id, name, email) VALUES (?, ?, ?)',
                [(int(u['id']), u['name'], u['email']) for u in users])
            connection.executemany(
                'INSERT INTO guests(id, name, email) VALUES (?, ?, ?)',
                [(int(g['id']), g['name'], g['email']) for g in guests])
            connection.executemany(
                'INSERT INTO events(id, name, date, user_id) VALUES (?, ?, ?, ?)',
                [(int(e['id']), e['name'], e['date'],
                  int(e['user_id']) if e.get('user_id') is not None
                  and int(e['user_id']) in user_ids else None) for e in events])
            connection.executemany(
                '''INSERT INTO invitations(id, event_id, guest_id, guest_name, response, status)
                   VALUES (?, ?, ?, ?, ?, ?)''',
                [(int(i['id']), int(i['event_id']),
                  int(i['guest_id']) if i.get('guest_id') is not None
                  and int(i['guest_id']) in guest_ids else None,
                  i.get('guest_name') or 'Неизвестный гость',
                  i.get('response', 'не знаю'), i.get('status', 'active')) for i in invitations])
        return dict(users=len(users), guests=len(guests), events=len(events),
                    invitations=len(invitations))
    finally:
        connection.close()


def main():
    parser = argparse.ArgumentParser(description='Импорт JSON в SQLite для ПР7')
    parser.add_argument('--data-dir', type=Path, default=ROOT_DIR / 'data')
    parser.add_argument('--database', type=Path, default=DB_PATH)
    args = parser.parse_args()
    counts = import_json(args.data_dir, args.database)
    print(f'База {args.database} обновлена: {counts}')


if __name__ == '__main__':
    main()
