from django.urls import path

from . import views

urlpatterns = [
    path("", views.invitations, name="invitations"),
    path(
        "<int:invitation_id>/",
        views.invitation_detail,
        name="invitation_detail",
    ),
]
