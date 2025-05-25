from django.contrib import admin
from .models import Agent, Space, Event

@admin.register(Agent)
class AgentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'name', 'email']
    search_fields = ['name', 'email', 'user__username']
    list_filter = ['user__is_active']

@admin.register(Space)
class SpaceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'location']
    search_fields = ['name']
    list_filter = []

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'start', 'end']
    search_fields = ['title']
    list_filter = ['start']