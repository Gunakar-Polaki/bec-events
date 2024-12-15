from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.user_register, name='user_register'),
    path('login/', views.user_login, name='user_login'),
    path('logout/', views.user_logout, name='user_logout'),
    path('events/', views.event_list, name='event_list'),
    path('register/<int:event_id>/', views.event_register, name='event_register'),
    path('download_data/', views.download_data, name='download_data'),
    path('addevent/', views.addevent, name='addevent'),
    path('delete-event/<int:event_id>/', views.delete_event, name='delete_event'),
]
