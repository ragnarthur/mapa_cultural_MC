# core/test.py

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User, Group
from .models import Agent

class UserFlowsTest(TestCase):
    def setUp(self):
        # cria grupo de administrador
        admin_group, _ = Group.objects.get_or_create(name='Administrador')
        # cria um usuário admin
        self.admin = User.objects.create_user(
            username='admin',
            password='teste123',
            is_staff=True
        )
        self.admin.groups.add(admin_group)

    def test_signup_and_login(self):
        # signup
        resp = self.client.post(reverse('signup'), {
            'username': 'novo',
            'name': 'Novo Usuário',
            'email': 'novo@ex.com',
            'password1': 'Complex@123',
            'password2': 'Complex@123',
        })
        self.assertRedirects(resp, reverse('home'))

        # login
        login_ok = self.client.login(username='novo', password='Complex@123')
        self.assertTrue(login_ok)

    def test_agent_crud(self):
        # login como admin
        self.client.login(username='admin', password='teste123')

        # criar Agent
        resp = self.client.post(reverse('agent_create'), {
            'name': 'Teste', 'email': 't@t.com'
        })
        self.assertRedirects(resp, reverse('agent_list'))

        # listar Agents
        resp = self.client.get(reverse('agent_list'))
        self.assertContains(resp, 'Teste')

        # editar Agent
        agent = Agent.objects.get(name='Teste')
        resp = self.client.post(
            reverse('agent_update', args=[agent.pk]),
            {'name': 'Teste2', 'email': 't2@t.com'}
        )
        self.assertRedirects(resp, reverse('agent_list'))
        agent.refresh_from_db()
        self.assertEqual(agent.name, 'Teste2')

        # excluir Agent
        resp = self.client.post(
            reverse('agent_delete', args=[agent.pk])
        )
        self.assertRedirects(resp, reverse('agent_list'))
        self.assertFalse(Agent.objects.filter(pk=agent.pk).exists())
