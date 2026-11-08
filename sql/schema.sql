-- ПР7: separate legacy domain SQLite database. PR9 uses Django migrations.
PRAGMA foreign_keys = ON;
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS guests (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY, name TEXT NOT NULL, date TEXT NOT NULL,
    user_id INTEGER REFERENCES users(id) ON DELETE SET NULL
);
CREATE TABLE IF NOT EXISTS invitations (
    id INTEGER PRIMARY KEY,
    event_id INTEGER NOT NULL REFERENCES events(id) ON DELETE CASCADE,
    guest_id INTEGER REFERENCES guests(id) ON DELETE SET NULL,
    guest_name TEXT NOT NULL, response TEXT NOT NULL DEFAULT 'не знаю',
    status TEXT NOT NULL DEFAULT 'active'
);
CREATE INDEX IF NOT EXISTS idx_events_date ON events(date);
CREATE INDEX IF NOT EXISTS idx_events_user ON events(user_id);
CREATE INDEX IF NOT EXISTS idx_invitations_event_status ON invitations(event_id, status);
CREATE INDEX IF NOT EXISTS idx_invitations_guest ON invitations(guest_id);
