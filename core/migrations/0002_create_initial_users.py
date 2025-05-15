# core/migrations/0002_create_initial_users.py
from django.db import migrations

def create_initial_users(apps, schema_editor):
    User = apps.get_model('auth', 'User')

    # limpa antes de recriar (caso haja)
    User.objects.filter(username__in=['admin', 'editor', 'usuario_teste']).delete()

    # superusuário: usa create_superuser (gera hash corretamente)
    User.objects.create_superuser(
        username='admin',
        email='admin@exemplo.com',
        password='teste123'
    )

    # editor: staff mas não superuser
    editor = User.objects.create_user(
        username='editor',
        email='editor@exemplo.com',
        password='editor123'
    )
    editor.is_staff = True
    editor.save()

    # usuário comum
    User.objects.create_user(
        username='usuario_teste',
        email='usuario@exemplo.com',
        password='usuario123'
    )

class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_initial_users),
    ]
