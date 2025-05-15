# core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('',                         views.home,           name='home'),

    # Cadastro de usuário (registro)
    path('signup/', views.signup, name='signup'),

    # CRUD de Agentes
    path('agents/',                  views.agent_list,     name='agent_list'),
    path('agents/criar/',            views.agent_create,   name='agent_create'),
    path('agents/<int:pk>/editar/',  views.agent_update,   name='agent_update'),
    path('agents/<int:pk>/excluir/', views.agent_delete,   name='agent_delete'),

    # CRUD de Espaços
    path('spaces/',                  views.space_list,     name='space_list'),
    path('spaces/criar/',            views.space_create,   name='space_create'),
    path('spaces/<int:pk>/editar/',  views.space_update,   name='space_update'),
    path('spaces/<int:pk>/excluir/', views.space_delete,   name='space_delete'),

    # CRUD de Eventos
    path('events/',                  views.event_list,     name='event_list'),
    path('events/criar/',            views.event_create,   name='event_create'),
    path('events/<int:pk>/editar/',  views.event_update,   name='event_update'),
    path('events/<int:pk>/excluir/', views.event_delete,   name='event_delete'),
]
