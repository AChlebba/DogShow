from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('shows/', views.shows, name='shows'),
    path('login/', views.loginUser, name='login'),
    path('register/', views.registerUser, name='register'),
    path('logout/', views.logoutUser, name='logout'),
    path('user-profile/', views.userProfile, name='user-profile'),
    path('new-dog/', views.newDog, name='new-dog'),
    path('submit-dog/<str:pk>', views.submitDog, name='submit-dog'),
    path('cancel-dog/<str:pk>/<str:dpk>', views.cancelDog, name='cancel-dog'),
    path('delete-dog/<str:pk>', views.deleteDog, name='delete-dog'),
    path('dog-profile/<str:pk>', views.dogProfile, name='dog-profile'),
    path('shows-details/<str:pk>', views.showsDetails, name='shows-details'),
]