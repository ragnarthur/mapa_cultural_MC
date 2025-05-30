from django.contrib.auth.models import User
from django.db import models

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='agent_profile')
    name = models.CharField("Nome", max_length=200)
    email = models.EmailField("E-mail")
    area_of_activity = models.CharField("Área de Atuação", max_length=200, blank=True, help_text="Ex: Música, Dança, Artes Visuais…")
    education = models.CharField("Formação Cultural", max_length=200, blank=True, help_text="Ex: Bacharel em Música, Técnico em Teatro…")
    bio = models.TextField("Biografia / Descrição", blank=True, help_text="Conte aqui um breve histórico ou currículo resumido.")
    contact = models.CharField("Telefone / Contato", max_length=100, blank=True, help_text="Telefone, WhatsApp ou outra forma de contato.")
    portfolio_pdf = models.FileField(upload_to='portfolios/', blank=True, null=True)
    photo = models.ImageField(
        upload_to='agents/photos/', blank=True, null=True,
        verbose_name='Foto do agente')
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField("Criado em", auto_now_add=True)
    updated_at = models.DateTimeField("Última atualização", auto_now=True)

    def __str__(self):
        return f"{self.name} — {self.area_of_activity or 'Sem área definida'}"

class Space(models.Model):
    name = models.CharField(max_length=200)
    location = models.CharField(max_length=100, help_text='Coordenadas em "lat,lng" ou descrição do local')
    desc = models.TextField(blank=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    start = models.DateTimeField()
    end = models.DateTimeField()
    approved = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class EmailVerification(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=8)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
