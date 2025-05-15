# mapas_culturais/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Painel de administração
    path('admin/', admin.site.urls),

    # Rotas de autenticação Django (login/logout, password change/reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Rotas do aplicativo core
    path('', include('core.urls')),
]
