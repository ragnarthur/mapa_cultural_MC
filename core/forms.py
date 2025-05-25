from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Agent, Space, Event

class RegistrationForm(UserCreationForm):
    name  = forms.CharField(
        label="Nome completo",
        max_length=200,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    email = forms.EmailField(
        label="E-mail",
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model  = User
        fields = ['username', 'name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Criação do perfil do agente pode ser feita após email verificado
        return user

class AgentForm(forms.ModelForm):
    class Meta:
        model = Agent
        fields = [
            'name', 'email',
            'area_of_activity', 'education',
            'bio', 'contact',
            'portfolio_pdf',
        ]
        widgets = {
            'name':             forms.TextInput(attrs={'class': 'form-control'}),
            'email':            forms.EmailInput(attrs={'class': 'form-control'}),
            'area_of_activity': forms.TextInput(attrs={'class': 'form-control'}),
            'education':        forms.TextInput(attrs={'class': 'form-control'}),
            'bio':              forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'contact':          forms.TextInput(attrs={'id': 'contact', 'class': 'form-control', 'placeholder': '(XX)XXXXX-XXXX'}),
            'portfolio_pdf':    forms.ClearableFileInput(attrs={'accept': '.pdf'}),
        }

        # Validação: aceita apenas PDF (opcional, mas recomendado)
    def clean_portfolio_pdf(self):
        pdf = self.cleaned_data.get('portfolio_pdf')
        if pdf and not pdf.name.lower().endswith('.pdf'):
            raise forms.ValidationError("Envie apenas arquivos em PDF.")
        return pdf

class SpaceForm(forms.ModelForm):
    class Meta:
        model  = Space
        fields = ['name', 'location', 'desc']
        widgets = {
            'name':      forms.TextInput(attrs={'class': 'form-control'}),
            'location':  forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'lat,lng'}),
            'desc':      forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def clean_location(self):
        """
        Garante que o campo será salvo como 'lat,lng', sem espaços.
        """
        location = self.cleaned_data['location'].replace(" ", "")
        # Opcional: pode validar se está no formato correto.
        if ',' not in location:
            raise forms.ValidationError("Digite no formato: latitude,longitude (ex: -18.73149950768294,-47.4982353736)")
        lat, lng = location.split(',', 1)
        try:
            float(lat)
            float(lng)
        except ValueError:
            raise forms.ValidationError("Latitude e longitude devem ser números válidos.")
        return location


class EventForm(forms.ModelForm):
    class Meta:
        model  = Event
        fields = ['title', 'start', 'end']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'start': forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local'
            }),
            'end':   forms.DateTimeInput(attrs={
                'class': 'form-control', 'type': 'datetime-local'
            }),
        }
