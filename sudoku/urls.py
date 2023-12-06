from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create_room', views.create_room, name='create_room'),
    path('room/<str:room_name>', views.join_room, name='join_room'),
    path('check_tile/<str:room_name>/<int:col>/<int:row>/<str:value>', views.check_tile, name='check_tile'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),

]
