from django.urls import path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('signup/', views.signup, name='signup'),
    path('verify_email/', views.verify_email, name='verify_email'),

    # Agentes
    path('agents/', views.agent_list, name='agent_list'),
    path('agents/criar/', views.agent_create, name='agent_create'),
    path('agents/<int:pk>/editar/', views.agent_update, name='agent_update'),
    path('agents/<int:pk>/excluir/', views.agent_delete, name='agent_delete'),
    path('agents/<int:pk>/aprovar/', views.agent_approve, name='agent_approve'),
    path('agents/pendentes/', views.agent_pending_list, name='agent_pending_list'),

    # Espaços
    path('spaces/', views.space_list, name='space_list'),
    path('spaces/criar/', views.space_create, name='space_create'),
    path('spaces/<int:pk>/editar/', views.space_update, name='space_update'),
    path('spaces/<int:pk>/excluir/', views.space_delete, name='space_delete'),
    path('spaces/<int:pk>/aprovar/', views.space_approve, name='space_approve'),
    path('spaces/pendentes/', views.space_pending_list, name='space_pending_list'),

    # Eventos
    path('events/', views.event_list, name='event_list'),
    path('events/criar/', views.event_create, name='event_create'),
    path('events/<int:pk>/editar/', views.event_update, name='event_update'),
    path('events/<int:pk>/excluir/', views.event_delete, name='event_delete'),
    path('events/<int:pk>/aprovar/', views.event_approve, name='event_approve'),
    path('events/pendentes/', views.event_pending_list, name='event_pending_list'),


    path('admin/', admin.site.urls),
    path('api/', include('core.api_urls')),
]
