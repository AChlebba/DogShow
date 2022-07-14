from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shows/', views.shows, name='shows'),
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('user-profile/', views.userProfile, name='user-profile'),
    path('shows-details/<str:pk>', views.showsDetails, name='shows-details'),
]