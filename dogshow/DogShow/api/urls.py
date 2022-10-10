from django.urls import path
from . import views

urlpatterns = [
    path('api/urls', views.apiUrls),
    path('api/', views.apiRoot),
    
    path('api/user-list/', views.userList, name='user-list'),
    path('api/user-detail/<str:pk>', views.userDetail, name='user-detail'),

    path('api/dog-list/', views.dogList, name="dog-list"),
    path('api/dog-detail/<str:pk>', views.dogDetail, name='dog-detail'),

    path('api/show-list/', views.showList, name='show-list'),
    path('api/show-detail/<str:pk>', views.showDetail, name='show-detail'),

    path('api/score-list/', views.scoreList, name='score-list'),
    path('api/score-detail/<str:pk>', views.scoreDetail, name='score-detail'),

    path('api/message-list/', views.messageList, name='message-list'),
    path('api/message-detail/<str:pk>', views.messageDetail, name='message-detail'),
]