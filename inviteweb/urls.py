"""Пути приложения с пространствами имён для Django {% url %}."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),
    path('events/', include('events_web.urls')),
    path('invitations/', include('invitations_web.urls')),
    path('users/', include('users_web.urls')),
    path('guests/', include('guests_web.urls')),
]
