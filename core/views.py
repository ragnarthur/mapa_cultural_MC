# core/views.py

from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Agent, Space, Event
from .forms import AgentForm, SpaceForm, EventForm, RegistrationForm

def home(request):
    return render(request, 'core/home.html')

# ——— CRUD Agent ———

@login_required
@permission_required('core.view_agent', raise_exception=True)
def agent_list(request):
    agents = Agent.objects.all()
    return render(request, 'core/agent_list.html', {'agents': agents})

@login_required
@permission_required('core.add_agent', raise_exception=True)
def agent_create(request):
    form = AgentForm(request.POST or None)
    if form.is_valid():
        agent = form.save(commit=False)
        agent.user = request.user
        agent.save()
        return redirect('agent_list')
    return render(request, 'core/agent_form.html', {
        'form': form,
        'action': 'Criar'
    })

@login_required
@permission_required('core.change_agent', raise_exception=True)
def agent_update(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    form  = AgentForm(request.POST or None, instance=agent)
    if form.is_valid():
        form.save()
        return redirect('agent_list')
    return render(request, 'core/agent_form.html', {
        'form': form,
        'action': 'Editar'
    })

@login_required
@permission_required('core.delete_agent', raise_exception=True)
def agent_delete(request, pk):
    agent = get_object_or_404(Agent, pk=pk)
    if request.method == 'POST':
        agent.delete()
        return redirect('agent_list')
    return render(request, 'core/agent_confirm_delete.html', {
        'agent': agent
    })

# ——— CRUD Space ———

@login_required
@permission_required('core.view_space', raise_exception=True)
def space_list(request):
    spaces = Space.objects.all()
    return render(request, 'core/space_list.html', {'spaces': spaces})

@login_required
@permission_required('core.add_space', raise_exception=True)
def space_create(request):
    form = SpaceForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('space_list')
    return render(request, 'core/space_form.html', {
        'form': form,
        'action': 'Criar'
    })

@login_required
@permission_required('core.change_space', raise_exception=True)
def space_update(request, pk):
    space = get_object_or_404(Space, pk=pk)
    form  = SpaceForm(request.POST or None, instance=space)
    if form.is_valid():
        form.save()
        return redirect('space_list')
    return render(request, 'core/space_form.html', {
        'form': form,
        'action': 'Editar'
    })

@login_required
@permission_required('core.delete_space', raise_exception=True)
def space_delete(request, pk):
    space = get_object_or_404(Space, pk=pk)
    if request.method == 'POST':
        space.delete()
        return redirect('space_list')
    return render(request, 'core/space_confirm_delete.html', {
        'space': space
    })

# ——— CRUD Event ———

@login_required
@permission_required('core.view_event', raise_exception=True)
def event_list(request):
    events = Event.objects.all()
    return render(request, 'core/event_list.html', {'events': events})

@login_required
@permission_required('core.add_event', raise_exception=True)
def event_create(request):
    form = EventForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'core/event_form.html', {
        'form': form,
        'action': 'Criar'
    })

@login_required
@permission_required('core.change_event', raise_exception=True)
def event_update(request, pk):
    event = get_object_or_404(Event, pk=pk)
    form  = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('event_list')
    return render(request, 'core/event_form.html', {
        'form': form,
        'action': 'Editar'
    })

@login_required
@permission_required('core.delete_event', raise_exception=True)
def event_delete(request, pk):
    event = get_object_or_404(Event, pk=pk)
    if request.method == 'POST':
        event.delete()
        return redirect('event_list')
    return render(request, 'core/event_confirm_delete.html', {
        'event': event
    })

# ——— User Registration ———

def signup(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = RegistrationForm()
    return render(request, 'registration/signup.html', {'form': form})
