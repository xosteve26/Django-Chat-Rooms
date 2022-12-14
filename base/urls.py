from django.urls import path
from . import views

urlpatterns = [
    path('login', views.login_page, name='login'),
    path('register', views.register_page, name='register'),
    path('', views.home, name='home'),
    path('room/<str:room_id>', views.room, name='room'),
    path('create_room', views.create_room, name='create_room'),
    path('edit_room/<str:room_id>', views.edit_room, name='edit_room'),
    path('delete_room/<str:room_id>', views.delete_room, name='delete_room'),
    path('delete_message/<str:message_id>', views.delete_message, name='delete_message'),
    path('update-user/', views.updateUser, name='update-user'),
    path('topics/', views.topicsPage, name='topics'),
    path('user-profile/<str:user_id>', views.userProfile, name='user-profile'),
    path('logout', views.logout_page, name='logout'),
]
