from rest_framework import serializers
from django.contrib.auth.models import User, Group
from base.models import Dog, Show, Score, Message


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'profile', 'groups', 'email', 'date_joined', 'last_login']
        depth = 1


class DogSerializer(serializers.HyperlinkedModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Dog
        fields = '__all__'


class ShowSerializer(serializers.ModelSerializer):
    referee1 = serializers.ReadOnlyField(source='referee1.username')
    referee2 = serializers.ReadOnlyField(source='referee2.username')
    referee3 = serializers.ReadOnlyField(source='referee3.username')

    class Meta:
        model = Show
        fields = '__all__'
        depth = 1


class ScoreSerializer(serializers.ModelSerializer):
    referee = serializers.ReadOnlyField(source='referee.username')

    class Meta:
        model = Score
        fields = '__all__'
        depth = 1


class MessageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Message
        fields = '__all__'
