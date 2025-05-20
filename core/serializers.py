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
    lat = serializers.SerializerMethodField()
    lng = serializers.SerializerMethodField()

    class Meta:
        model = Space
        fields = ['id', 'name', 'location', 'lat', 'lng', 'desc', 'approved']

    def get_lat(self, obj):
        try:
            return float(obj.location.split(',')[0].strip())
        except:
            return None

    def get_lng(self, obj):
        try:
            return float(obj.location.split(',')[1].strip())
        except:
            return None
        
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'title', 'start', 'end', 'approved']
