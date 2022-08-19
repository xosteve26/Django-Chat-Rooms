from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('room/<str:room_id>', views.room, name='room'),
    path('create_room', views.create_room, name='create_room'),
    path('edit_room/<str:room_id>', views.edit_room, name='edit_room'),
    path('delete_room/<str:room_id>', views.delete_room, name='delete_room'),
]
