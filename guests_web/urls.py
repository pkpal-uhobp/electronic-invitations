from django.urls import path
from . import views
app_name = 'guests'
urlpatterns = [
    path('', views.guests, name='list'),
    path('<int:guest_id>/', views.guest_detail, name='detail'),
]
