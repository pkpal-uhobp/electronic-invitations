
"""Работа с электронными приглашениями."""
from models import Invitation, Event
VALID_RESPONSES={"да","нет","не знаю"}

def add_invitation(invitations:list[Invitation], event:Event, guest_name:str)->Invitation:
    if not guest_name.strip():
        raise ValueError("Имя гостя не может быть пустым")
    item=Invitation(str(max((int(i.id) for i in invitations),default=0)+1),event,guest_name.strip())
    invitations.append(item)
    return item

def cancel_invitation(invitations:list[Invitation], invitation_id:str)->bool:
    for i in invitations:
        if i.id==invitation_id:
            i.cancel()
            return True
    return False

def set_response(invitations:list[Invitation], invitation_id:str, response:str)->bool:
    if response not in VALID_RESPONSES: raise ValueError("Допустимые ответы: да, нет, не знаю")
    for i in invitations:
        if i.id==invitation_id:
            i.set_response(response); return True
    return False

def sort_invitations(invitations):
    return sorted(invitations,key=lambda i:(i.guest_name.lower(),int(i.id)))

def find_invitations(invitations,query):
    return [i for i in invitations if query.lower() in i.guest_name.lower()]

def create_invitation(event_name, guest_name, event_date):
    return f"Здравствуйте, {guest_name}!\nПриглашаем вас на событие «{event_name}».\nДата проведения: {event_date}."

def process_response(response):
    return {"да":"Гость подтвердил участие.","нет":"Гость отказался от участия."}.get(response,"Ответ гостя пока не определён.")

def invitation_statistics(invitations):
    return {"total":len(invitations)}
