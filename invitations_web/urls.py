from django.urls import path
from . import views

app_name = 'invitations'
urlpatterns = [
    path('', views.invitations, name='list'),
    path('statistics/', views.statistics, name='statistics'),
    path('<int:invitation_id>/', views.invitation_detail, name='detail'),
]
