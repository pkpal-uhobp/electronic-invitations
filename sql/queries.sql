-- ПР7 legacy 19 named queries. Django PR9 views no longer call these.
-- name: users_list
SELECT id, name, email FROM users ORDER BY name, id;
-- name: guests_list
SELECT id, name, email FROM guests ORDER BY name, id;
-- name: events_list
SELECT e.id, e.name, e.date, e.user_id,
       u.name AS organizer_name, u.email AS organizer_email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id
ORDER BY e.date, e.name, e.id;
-- name: invitations_list
SELECT i.id, i.event_id, i.guest_id, i.guest_name,
       i.status, i.response, e.name AS event_name, e.date AS event_date,
       g.name AS guest_real_name, g.email AS guest_email
FROM invitations AS i JOIN events AS e ON e.id = i.event_id
LEFT JOIN guests AS g ON g.id = i.guest_id ORDER BY i.id;
-- name: event_by_id
SELECT e.id, e.name, e.date, e.user_id,
       u.name AS organizer_name, u.email AS organizer_email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id WHERE e.id = ?;
-- name: invitation_by_id
SELECT i.id, i.event_id, i.guest_id, i.guest_name,
       i.status, i.response, e.name AS event_name, e.date AS event_date,
       g.name AS guest_real_name, g.email AS guest_email
FROM invitations AS i JOIN events AS e ON e.id = i.event_id
LEFT JOIN guests AS g ON g.id = i.guest_id WHERE i.id = ?;
-- name: user_by_id
SELECT id, name, email FROM users WHERE id = ?;
-- name: guest_by_id
SELECT id, name, email FROM guests WHERE id = ?;
-- name: events_on_date
SELECT e.id, e.name, e.date, e.user_id,
       u.name AS organizer_name, u.email AS organizer_email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id
WHERE e.date = ? ORDER BY e.name, e.id;
-- name: available_guests
SELECT g.id, g.name, g.email FROM guests AS g WHERE NOT EXISTS (
 SELECT 1 FROM invitations AS i WHERE i.guest_id = g.id AND i.event_id = ?
 AND i.status = 'active'
) ORDER BY g.name, g.id;
-- name: invitations_by_status
SELECT i.id, i.event_id, i.guest_id, i.guest_name,
       i.status, i.response, e.name AS event_name, e.date AS event_date,
       g.name AS guest_real_name, g.email AS guest_email
FROM invitations AS i JOIN events AS e ON e.id = i.event_id
LEFT JOIN guests AS g ON g.id = i.guest_id
WHERE i.status = ? ORDER BY i.id;
-- name: invitations_for_guest
SELECT i.id, i.event_id, i.guest_id, i.guest_name,
       i.status, i.response, e.name AS event_name, e.date AS event_date,
       g.name AS guest_real_name, g.email AS guest_email
FROM invitations AS i JOIN events AS e ON e.id = i.event_id
LEFT JOIN guests AS g ON g.id = i.guest_id
WHERE i.guest_id = ? ORDER BY i.id;
-- name: events_for_user
SELECT e.id, e.name, e.date, e.user_id,
       u.name AS organizer_name, u.email AS organizer_email
FROM events AS e LEFT JOIN users AS u ON u.id = e.user_id
WHERE e.user_id = ? ORDER BY e.date, e.id;
-- name: total_counts
SELECT (SELECT COUNT(*) FROM events) AS events,
       (SELECT COUNT(*) FROM invitations) AS invitations,
       (SELECT COUNT(*) FROM users) AS users,
       (SELECT COUNT(*) FROM guests) AS guests;
-- name: invitation_totals
SELECT COUNT(*) AS total,
       COALESCE(SUM(CASE WHEN status = 'active' THEN 1 ELSE 0 END), 0) AS active,
       COALESCE(SUM(CASE WHEN status = 'cancelled' THEN 1 ELSE 0 END), 0) AS cancelled,
       COALESCE(SUM(CASE WHEN response = 'да' THEN 1 ELSE 0 END), 0) AS yes_count
FROM invitations;
-- name: invitations_by_event
SELECT e.id, e.name, COUNT(i.id) AS invitation_count,
       COUNT(CASE WHEN i.status = 'active' THEN 1 END) AS active_count
FROM events AS e LEFT JOIN invitations AS i ON i.event_id = e.id
GROUP BY e.id, e.name ORDER BY invitation_count DESC, e.id;
-- name: invitations_by_response
SELECT response, COUNT(*) AS invitation_count FROM invitations
GROUP BY response ORDER BY invitation_count DESC, response;
-- name: organizer_event_counts
SELECT u.id, u.name, COUNT(e.id) AS event_count
FROM users AS u LEFT JOIN events AS e ON e.user_id = u.id
GROUP BY u.id, u.name ORDER BY event_count DESC, u.id;
-- name: popular_events
SELECT e.id, e.name, COUNT(i.id) AS invitation_count
FROM events AS e JOIN invitations AS i ON i.event_id = e.id
GROUP BY e.id, e.name HAVING COUNT(i.id) >= ?
ORDER BY invitation_count DESC, e.id;
