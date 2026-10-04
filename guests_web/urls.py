from django.urls import path

from . import views

urlpatterns = [
    path("", views.guests, name="guests"),
    path("<int:guest_id>/", views.guest_detail, name="guest_detail"),
]
