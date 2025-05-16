from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Agent, Space, Event

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class AgentSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Agent
        fields = [
            'id', 'user', 'name', 'email',
            'area_of_activity', 'education',
            'bio', 'contact', 'approved',
            'created_at', 'updated_at'
        ]

class SpaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Space
        fields = ['id', 'name', 'location', 'desc', 'approved']

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start', 'end', 'approved']
