from django.urls import path
from . import views

app_name = 'events'
urlpatterns = [
    path('', views.events, name='list'),
    path('search/', views.search_by_date, name='search'),
    path('available/', views.available_guests, name='available'),
    path('<int:event_id>/', views.event_detail, name='detail'),
]
