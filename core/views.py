from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from core.models import Evento
# Create your views here.
# def LocalEvento(request, nome):
#     return HttpResponse('O local do evento é {}'.format(local))
def submit_login(request):
    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')
        usuario = authenticate(username=username, password=password)
        if usuario is not None:
            login(request, usuario)
        else:
            messages.error(request, message='usuário ou senha inválido')
    return redirect('/')

def login_usuario(request):
    return render(request, 'login.html')

def logout_usuario(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def lista_eventos(request):
    usuario = request.user
    evento = Evento.objects.filter(usuario=usuario)
    dados = {'eventos':evento}
    return render(request, 'agenda.html', dados)

@login_required(login_url='/login')
def evento(request):
    id_evento = request.GET.get('id')
    dados = {}
    if id_evento:
        dados['evento'] = Evento.objects.get(id=id_evento)
    return render(request, 'evento.html', dados)

@login_required(login_url='/login')
def submit_evento(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        descricao = request.POST.get('descricao')
        data_evento = request.POST.get('data_evento')
        usuario = request.user
        local = request.POST.get('local')
        id_evento = request.POST.get('id_evento')
        if id_evento:
            evento = Evento.objects.get(id=id_evento)
            if usuario == evento.usuario:
                evento.titulo = titulo
                evento.descricao = descricao
                evento.data_evento = data_evento
                evento.local = local
                evento.save()
            # Evento.objects.filter(id=id_evento).update(
            #                         titulo=titulo, 
            #                         descricao=descricao,
            #                         data_evento=data_evento,
            #                         local=local)
        else:
            Evento.objects.create(  titulo=titulo, 
                                    descricao=descricao,
                                    data_evento=data_evento,
                                    usuario=usuario,
                                    local=local)
    return redirect('/')
@login_required(login_url='/login')
def delete_evento(request,id_evento):
    usuario = request.user
    evento = Evento.objects.get(id=id_evento)
    if usuario == evento.usuario:
        evento.delete()
    return redirect('/')