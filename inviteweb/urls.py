"""Existing routes preserved from PR6/PR7."""
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
handler400 = 'inviteweb.error_views.bad_request'
handler403 = 'inviteweb.error_views.permission_denied'
handler404 = 'inviteweb.error_views.page_not_found'
handler500 = 'inviteweb.error_views.server_error'
