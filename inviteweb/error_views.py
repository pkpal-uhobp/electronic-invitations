"""Брендированные HTTP-страницы ошибок с правильными HTTP-кодами."""
from django.http import HttpResponseServerError
from django.shortcuts import render
from django.template.loader import render_to_string


def bad_request(request, exception):
    return render(request, '400.html', status=400)


def permission_denied(request, exception):
    return render(request, '403.html', status=403)


def page_not_found(request, exception):
    return render(request, '404.html', status=404)


def server_error(request):
    # Для ошибки 500 не вызываем контекстные процессоры, которые могли упасть.
    html = render_to_string('500.html')
    return HttpResponseServerError(html)
