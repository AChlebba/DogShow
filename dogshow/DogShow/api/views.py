from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import renderers
from rest_framework import generics
from rest_framework import viewsets

from django.contrib.auth.models import User, Group
from base.models import Dog, Show, Score, Message
from .serializers import UserSerializer, DogSerializer, ShowSerializer, ScoreSerializer, MessageSerializer

@api_view(['GET'])
def apiUrls(request):
    if request.method == 'GET':
        api_urls = {
            "Users": "/user-list",
            "User": "/user-detail/<id>",
            "Dogs": "/dog-list",
            "Dog": "/dog-detail/<id>",
            "Shows": "/show-list",
            "Show": "/show-detail/<id>",
            "Scores": "/score-list",
            "Score": "/score-detail/<id>",
            "Messages": "/message-list",
            "Message": "/message-detail/<id>",

        }
        return Response(api_urls)



@api_view(['GET'])
def apiRoot(request):
    return Response({
        'users': reverse('user-list', request=request),
        'dogs': reverse('dog-list', request=request),
        'shows': reverse('show-list', request=request),
        'scores': reverse('score-list', request=request),
        'message': reverse('message-list', request=request),
    })







@api_view(['GET'])
def userList(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def userDetail(request, pk):
    if request.method == 'GET':
        try:
            users = User.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = UserSerializer(users, context={'request': request}, many=False)
        return Response(serializer.data)



@api_view(['GET'])
def dogList(request):
    if request.method == 'GET':
        dogs = Dog.objects.all()
        serializer = DogSerializer(dogs, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def dogDetail(request, pk):
    if request.method == 'GET':
        try:
            dogs = Dog.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = DogSerializer(dogs, context={'request': request}, many=False)
        return Response(serializer.data)



@api_view(['GET'])
def showList(request):
    if request.method == 'GET':
        shows = Show.objects.all()
        serializer = ShowSerializer(shows, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def showDetail(request, pk):
    if request.method == 'GET':
        try:
            shows = Show.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
            
        serializer = ShowSerializer(shows, context={'request': request}, many=False)
        return Response(serializer.data)



@api_view(['GET'])
def scoreList(request):
    if request.method == 'GET':
        scores = Score.objects.all()
        serializer = ScoreSerializer(scores, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def scoreDetail(request, pk):
    if request.method == 'GET':
        try:
            scores = Score.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = ScoreSerializer(scores, context={'request': request}, many=False)
        return Response(serializer.data)



@api_view(['GET'])
def messageList(request):
    if request.method == 'GET':
        messages = Message.objects.all()
        serializer = MessageSerializer(messages, context={'request': request}, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def messageDetail(request, pk):
    if request.method == 'GET':
        try:
            messages = Message.objects.get(id=pk)
        except:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        serializer = MessageSerializer(messages, context={'request': request}, many=False)
        return Response(serializer.data)