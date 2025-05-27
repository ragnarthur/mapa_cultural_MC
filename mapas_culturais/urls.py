from django.conf import settings
from django.conf.urls.static import static
from django.urls import include, path
from django.contrib import admin

urlpatterns = [
    # Painel de administração
    path('admin/', admin.site.urls),

    # Rotas de autenticação Django (login/logout, password change/reset)
    path('accounts/', include('django.contrib.auth.urls')),

    # Rotas do aplicativo core
    path('', include('core.urls')),
    path('api/', include('core.api_urls')),
]

# Só adiciona essas rotas em desenvolvimento (DEBUG=True)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
    # Se você usa collectstatic em produção, troque STATICFILES_DIRS[0] por STATIC_ROOT

