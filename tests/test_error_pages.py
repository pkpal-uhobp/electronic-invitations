"""PR6/PR7 branded HTTP errors are not removed."""
import pytest
from django.test import Client, RequestFactory, override_settings
from inviteweb import error_views

pytestmark = pytest.mark.django_db


def test_unknown_url_404():
    with override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver']):
        response = Client().get('/not-existing/')
    assert response.status_code == 404
    assert 'Страница не найдена' in response.content.decode('utf-8')


def test_error_status_codes_and_no_tracebacks():
    request = RequestFactory().get('/err/')
    for status, handler in ((400, error_views.bad_request),
                            (403, error_views.permission_denied),
                            (404, error_views.page_not_found)):
        response = handler(request, Exception('private-error-detail'))
        assert response.status_code == status
        assert 'private-error-detail' not in response.content.decode('utf-8')
    assert error_views.server_error(request).status_code == 500
