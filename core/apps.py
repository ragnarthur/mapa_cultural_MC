from django.apps import AppConfig
from django.db.models.signals import post_migrate

class CoreConfig(AppConfig):
    name = 'core'

    def ready(self):
        post_migrate.connect(create_groups_and_perms, sender=self)

def create_groups_and_perms(sender, **kwargs):
    from django.contrib.auth.models import Group, Permission
    from django.contrib.contenttypes.models import ContentType
    from .models import Agent, Space, Event

    # Modelos alvo
    models = [Agent, Space, Event]
    # Cria ou obtém grupos
    admin_group, _  = Group.objects.get_or_create(name='Administrador')
    editor_group, _ = Group.objects.get_or_create(name='Editor')
    user_group, _   = Group.objects.get_or_create(name='Usuário')

    # Limpa permissões existentes (para reexecuções)
    admin_group.permissions.clear()
    editor_group.permissions.clear()
    user_group.permissions.clear()

    # Para cada modelo, pega ContentType e suas permissões
    for model in models:
        ct = ContentType.objects.get_for_model(model)
        perms = Permission.objects.filter(content_type=ct)

        # Administrador recebe todas as permissões
        admin_group.permissions.add(*perms)

        # Editor recebe add, change e view (sem delete)
        can_add    = perms.get(codename=f'add_{model._meta.model_name}')
        can_change = perms.get(codename=f'change_{model._meta.model_name}')
        can_view   = perms.get(codename=f'view_{model._meta.model_name}')
        editor_group.permissions.add(can_add, can_change, can_view)

        # Usuário recebe apenas view
        user_group.permissions.add(can_view)
