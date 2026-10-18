from datetime import date, timedelta
import pytest
from events import add_event, check_event, find_events, sort_events


def test_check_event_rejects_empty_name():
    assert not check_event('', date.today())


def test_add_event_and_find_event():
    events = {}
    event_id = add_event(events, 'День рождения', date.today()+timedelta(days=2))
    assert event_id == '1'
    assert find_events(events, 'рожд')[0][1]['name'] == 'День рождения'


def test_sort_events_by_date():
    events = {'1': {'name': 'Позже','date':'2026-12-10'},
              '2': {'name':'Раньше','date':'2026-10-10'}}
    assert [item[0] for item in sort_events(events)] == ['2','1']


def test_add_event_rejects_past_date():
    with pytest.raises(ValueError):
        add_event({}, 'Старое событие', date.today()-timedelta(days=1))
