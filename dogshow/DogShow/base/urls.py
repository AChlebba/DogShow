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
    path('add-show/', views.addShow, name='add-show'),
    path('add-referee/<str:pk>/<str:rpk>', views.addReferee, name='add-referee'),
    path('activate-show/<str:pk>', views.activateShow, name='activate-show'),
    path('score-page/<str:pk>/<str:dpk>', views.scorePage, name='score-page'),
    path('referees/', views.refereeList, name='referee-list'),
    path('referee-onoff/<str:pk>', views.refereeOnOff, name='referee-onoff'),
    path('chat/', views.chat, name='chat'),
    path('chat_refresh/', views.chatRefresh, name='chat-refresh'),
    path('dogs/', views.dogs, name='dogs'),
]