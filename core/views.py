from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from django.core.mail import send_mail
from django.conf import settings
from .models import Agent, Space, Event, EmailVerification
from .forms import AgentForm, SpaceForm, EventForm, RegistrationForm
from rest_framework import viewsets, permissions
from .serializers import AgentSerializer, SpaceSerializer, EventSerializer
import random
import json
import os  # <-- adicionado para o acesso ao arquivo
from django.http import FileResponse, Http404  # <-- adicionado

def home(request):
    return render(request, 'core/home.html')

# ----------- Cadastro e Verificação de Usuário -----------

def generate_code():
    return str(random.randint(100000, 999999))

def send_verification_email(user, code):
    subject = 'Verifique seu e-mail no Mapa Cultural de Monte Carmelo'
    message = (
        f"Olá, {user.username}!\n\n"
        "Obrigado por se cadastrar no Mapa Cultural de Monte Carmelo.\n"
        "Para ativar sua conta, use o código de verificação abaixo:\n\n"
        f"      Código de verificação: {code}\n\n"
        "Se você não solicitou este cadastro, pode ignorar este e-mail.\n\n"
        "Atenciosamente,\nEquipe Mapa Cultural de Monte Carmelo"
    )
    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )

def resend_verification_code(request):
    if request.method == "POST" or request.method == "GET":
        email = request.POST.get('email') or request.session.get('email_for_verification')
        if not email:
            messages.error(request, "Não foi possível identificar seu e-mail para reenviar o código.")
            return redirect('signup')
        user = User.objects.filter(email=email).order_by('-id').first()
        if not user:
            messages.error(request, "Usuário não encontrado para esse e-mail.")
            return redirect('signup')

        # Exclui códigos antigos deste usuário para evitar erro de unicidade
        EmailVerification.objects.filter(user=user).delete()

        # Gera novo código e envia novamente
        code = generate_code()
        EmailVerification.objects.create(user=user, code=code)
        send_verification_email(user, code)
        messages.success(request, "Um novo código de verificação foi enviado ao seu e-mail.")
        request.session['email_for_verification'] = email  # Mantém o e-mail na sessão
        return redirect('verify_email')
    else:
        return redirect('verify_email')
     
def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            code = generate_code()
            EmailVerification.objects.create(user=user, code=code)
            send_verification_email(user, code)
            # ----------- LINHA CRUCIAL: Salva e-mail na sessão -------------
            request.session['email_for_verification'] = user.email
            messages.info(request, "Cadastro criado com sucesso! Enviamos um código de verificação para seu e-mail. Por favor, verifique sua caixa de entrada e a pasta de spam/lixo eletrônico para ativar sua conta.")
            return redirect('verify_email')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})

def verify_email(request):
    if request.method == 'POST':
        code = request.POST.get('code')
        try:
            verification = EmailVerification.objects.get(code=code, verified=False)
            verification.verified = True
            verification.save()
            user = verification.user
            user.is_active = True
            user.save()
            messages.success(request, "E-mail verificado com sucesso! Agora você pode fazer login normalmente.")
            return redirect('login')
        except EmailVerification.DoesNotExist:
            messages.error(request, "Código inválido, expirado ou já utilizado. Tente novamente.")
    return render(request, 'registration/verify_email.html')


def superuser_required(view_func):
    return user_passes_test(lambda u: u.is_superuser)(view_func)

@login_required
@superuser_required
def agent_portfolio_list(request):
    agents = Agent.objects.filter(portfolio_pdf__isnull=False).exclude(portfolio_pdf='')
    return render(request, 'core/agent_portfolio_list.html', {'agents': agents})

@login_required
@superuser_required
def agent_portfolio_download(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if not agent.portfolio_pdf:
        raise Http404("Portfólio não encontrado.")
    file_path = agent.portfolio_pdf.path
    if not os.path.exists(file_path):
        raise Http404("Arquivo não encontrado.")
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response

# -------------- AGENTES --------------

@login_required
def agent_create(request):
    if not request.user.is_active:
        return redirect('login')
    if hasattr(request.user, 'agent_profile'):
        return redirect('agent_update', pk=request.user.agent_profile.pk)
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.user = request.user
            agent.approved = False
            agent.save()
            messages.success(request, "Perfil criado com sucesso! Aguarde aprovação da Secretaria.")
            return render(request, 'core/agent_awaiting_approval.html')
    else:
        form = AgentForm()
    return render(request, 'core/agent_form.html', {'form': form, 'action': 'Criar'})

@login_required
def agent_update(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if not (request.user.is_superuser or request.user == agent.user):
        return redirect('home')
    if request.method == "POST":
        form = AgentForm(request.POST, request.FILES, instance=agent)
        if form.is_valid():
            agent = form.save(commit=False)
            agent.approved = False
            agent.save()
            if request.user.is_superuser or request.user.has_perm('core.view_agent'):
                return redirect('agent_pending_list')
            else:
                return render(request, 'core/agent_awaiting_approval.html')
    else:
        form = AgentForm(instance=agent)
    return render(request, 'core/agent_form.html', {'form': form, 'action': 'Editar'})

@login_required
@permission_required('core.view_agent', raise_exception=True)
def agent_list(request):
    agents = Agent.objects.filter(approved=True)
    return render(request, 'core/agent_list.html', {'agents': agents})

@login_required
@permission_required('core.view_agent', raise_exception=True)
def agent_pending_list(request):
    pendentes = Agent.objects.filter(approved=False)
    return render(request, 'core/agent_pending_list.html', {'agents': pendentes})

@login_required
@permission_required('core.delete_agent', raise_exception=True)
def agent_delete(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.delete()
        return redirect('agent_list')
    return render(request, 'core/agent_confirm_delete.html', {'agent': agent})

@login_required
@permission_required('core.change_agent', raise_exception=True)
def agent_approve(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    agent.approved = True
    agent.save()
    return redirect('agent_pending_list')

@login_required
@user_passes_test(lambda u: u.is_superuser or u.has_perm('core.view_agent'))
def agent_portfolio_list(request):
    agents = Agent.objects.filter(portfolio_pdf__isnull=False).exclude(portfolio_pdf='')
    return render(request, 'core/agent_portfolio_list.html', {'agents': agents})

# NOVO: VIEW PARA VISUALIZAÇÃO/DOWNLOAD DO PDF DO PORTFÓLIO
@login_required
@user_passes_test(lambda u: u.is_superuser or u.has_perm('core.view_agent'))
def agent_portfolio_download(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if not agent.portfolio_pdf:
        raise Http404("Portfólio não encontrado.")
    file_path = agent.portfolio_pdf.path
    if not os.path.exists(file_path):
        raise Http404("Arquivo não encontrado.")
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename="{os.path.basename(file_path)}"'
    return response

# -------------- ESPAÇOS / EVENTOS --------------
@login_required
@permission_required('core.view_space', raise_exception=True)
def space_list(request):
    spaces = Space.objects.filter(approved=True)
    map_points = []
    for space in spaces:
        if ',' in space.location:
            lat, lng = space.location.split(',')
            map_points.append({
                "name": space.name,
                "lat": float(lat.strip()),
                "lng": float(lng.strip())
            })
    return render(request, 'core/space_list.html', {
        'spaces': spaces,
        'map_points_json': json.dumps(map_points)  # Só |safe no template
    })

@login_required
@permission_required('core.view_space', raise_exception=True)
def space_pending_list(request):
    pendentes = Space.objects.filter(approved=False)
    return render(request, 'core/space_pending_list.html', {'spaces': pendentes})

@login_required
@permission_required('core.add_space', raise_exception=True)
def space_create(request):
    form = SpaceForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Espaço cadastrado e aguardando aprovação.")
        return redirect('space_pending_list')
    return render(request, 'core/space_form.html', {'form': form, 'action': 'Criar'})

@login_required
@permission_required('core.change_space', raise_exception=True)
def space_update(request, pk):
    space = get_object_or_404(Space, pk=pk)
    form = SpaceForm(request.POST or None, instance=space)
    if form.is_valid():
        form.save()
        messages.success(request, "Espaço atualizado com sucesso!")
        return redirect('space_list') if space.approved else redirect('space_pending_list')
    return render(request, 'core/space_form.html', {'form': form, 'action': 'Editar'})

@login_required
@permission_required('core.delete_space', raise_exception=True)
def space_delete(request, pk):
    space = get_object_or_404(Space, pk=pk)
    if request.method == 'POST':
        space.delete()
        return redirect('space_list')
    return render(request, 'core/space_confirm_delete.html', {'space': space})

@login_required
@permission_required('core.change_space', raise_exception=True)
def space_approve(request, pk):
    space = get_object_or_404(Space, pk=pk)
    space.approved = True
    space.save()
    return redirect('space_pending_list')

# -------------- EVENTOS --------------
@login_required
@permission_required('core.view_event', raise_exception=True)
def event_list(request):
    events = Event.objects.filter(approved=True)
    return render(request, 'core/event_list.html', {'events': events})

@login_required
@permission_required('core.view_event', raise_exception=True)
def event_pending_list(request):
    pendentes = Event.objects.filter(approved=False)
    return render(request, 'core/event_pending_list.html', {'events': pendentes})

@login_required
@permission_required('core.add_event', raise_exception=True)
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        obj = form.save(commit=False)
        obj.save()
        messages.success(request, "Evento cadastrado e aguardando aprovação.")
        return redirect('event_pending_list')
    return render(request, 'core/event_form.html', {'form': form, 'action': 'Criar'})

@login_required
@permission_required('core.change_event', raise_exception=True)
def event_update(request, pk):
    evt = get_object_or_404(Event, pk=pk)
    form = EventForm(request.POST or None, instance=evt)
    if form.is_valid():  
        form.save()
        messages.success(request, "Evento atualizado com sucesso!")
        return redirect('event_list') if evt.approved else redirect('event_pending_list')
    return render(request, 'core/event_form.html', {'form': form, 'action': 'Editar'})

@login_required
@permission_required('core.delete_event', raise_exception=True)
def event_delete(request, pk):
    evt = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        evt.delete()
        return redirect('event_list')
    return render(request, 'core/event_confirm_delete.html', {'event': evt})

@login_required
@permission_required('core.change_event', raise_exception=True)
def event_approve(request, pk):
    evt = get_object_or_404(Event, pk=pk)
    evt.approved = True
    evt.save()
    return redirect('event_pending_list')

# ----------- API REST (DRF) ---------------

class AgentViewSet(viewsets.ModelViewSet):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user, approved=False)
    def perform_update(self, serializer):
        instance = serializer.save(approved=False)
        return instance

class SpaceViewSet(viewsets.ModelViewSet):
    queryset = Space.objects.all()
    serializer_class = SpaceSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(approved=False)
    def perform_update(self, serializer):
        instance = serializer.save(approved=False)
        return instance

class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def perform_create(self, serializer):
        serializer.save(approved=False)
    def perform_update(self, serializer):
        instance = serializer.save(approved=False)
        return instance
