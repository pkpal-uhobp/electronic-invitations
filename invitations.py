"""Создание и обработка электронных приглашений (совместимо с ПР3)."""
from models import Event, Guest, Invitation
VALID_RESPONSES = {"да", "нет", "не знаю"}

def _next_id(invitations):
    ids = [str(i['id'] if isinstance(i, dict) else i.id) for i in invitations]
    return str(max((int(i) for i in ids), default=0) + 1)

def _guest_name(guest):
    return guest.name if isinstance(guest, Guest) else str(guest)

def is_invitation_available(invitations, event_id, guest):
    event_id = str(getattr(event_id, 'id', event_id))
    guest_name = _guest_name(guest).strip().lower()
    for item in invitations:
        eid = str(item['event_id']) if isinstance(item, dict) else str(item.event.id)
        current_guest = item['guest_name'] if isinstance(item, dict) else item.guest_name
        status = item.get('status', 'active') if isinstance(item, dict) else item.status
        if eid == event_id and current_guest.strip().lower() == guest_name and status == 'active':
            return False
    return True

def add_invitation(invitations, event, guest):
    guest_name = _guest_name(guest).strip()
    if not guest_name:
        raise ValueError('Имя гостя не может быть пустым')
    if not is_invitation_available(invitations, event, guest):
        raise ValueError('Активное приглашение для гостя уже существует')
    ident = _next_id(invitations)
    if isinstance(event, Event):
        item = Invitation(ident, event, guest)
    else:
        item = {'id': ident, 'event_id': str(event), 'guest_name': guest_name, 'response': 'не знаю', 'status': 'active'}
    invitations.append(item)
    return item

def cancel_invitation(invitations, invitation_id):
    for item in invitations:
        if str(item['id'] if isinstance(item, dict) else item.id) == str(invitation_id):
            if isinstance(item, dict):
                item['status'] = 'cancelled'
            else:
                item.cancel()
            return True
    return False

def set_response(invitations, invitation_id, response):
    if response not in VALID_RESPONSES:
        raise ValueError('Допустимые ответы: да, нет, не знаю')
    for item in invitations:
        if str(item['id'] if isinstance(item, dict) else item.id) == str(invitation_id):
            if isinstance(item, dict):
                item['response'] = response
            else:
                item.set_response(response)
            return True
    return False

def sort_invitations(invitations):
    def key(i):
        return ((i['guest_name'] if isinstance(i, dict) else i.guest_name).lower(),
                int(i['id'] if isinstance(i, dict) else i.id))
    return sorted(invitations, key=key)

def find_invitations(invitations, query):
    return [i for i in invitations if query.lower() in
            (i['guest_name'] if isinstance(i, dict) else i.guest_name).lower()]

def find_invitation_by_id(invitations, invitation_id):
    return next((i for i in invitations if i.id == str(invitation_id)), None)

def create_invitation(event_name, guest_name, event_date):
    return (f'Здравствуйте, {guest_name}!\nПриглашаем вас на событие «{event_name}».\n'
            f'Дата проведения: {event_date}.')

def process_response(response):
    return {'да': 'Гость подтвердил участие.', 'нет': 'Гость отказался от участия.'}.get(
        response, 'Ответ гостя пока не определён.')

def invitation_statistics(invitations):
    stats={'total':len(invitations),'active':0,'cancelled':0,'yes':0,'no':0,'unknown':0}
    for i in invitations:
        status = i.get('status','active') if isinstance(i,dict) else i.status
        response = i.get('response','не знаю') if isinstance(i,dict) else i.response
        stats['active' if status == 'active' else 'cancelled'] += 1
        stats[{'да':'yes','нет':'no'}.get(response, 'unknown')] += 1
    return stats
