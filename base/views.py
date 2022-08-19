from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import Room, Topic, User
from .forms import RoomForm
from django.db.models import Q
# Create your views here.

rooms=None

def login_page(request):
    if request.method == "POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,'User does not exist')

        user=authenticate(request,username=username, password=password)

        if user:
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('/login')

    return render(request, 'base/login_register.html')

def home(request):
    params=request.GET.get('q')
    if params:
        rooms=Room.objects.filter(
            Q(topic__name__icontains=params) |
            Q(name__icontains=params) | 
            Q(description__icontains=params)
        )
    else:
        rooms=Room.objects.all()
    topics=Topic.objects.all()
    count=rooms.count()
    payload={'rooms':rooms, 'topics':topics,'room_count':count}
    
    return render(request, 'base/home.html', payload)


def room(request, room_id):
    room=Room.objects.get(id=room_id)
    payload={'room':room}
    return render(request, 'base/room.html', payload)

@login_required(login_url='/login')
def create_room(request):
    form=RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    payload={'form':form}
    return render(request, 'base/room_form.html', payload)


@login_required(login_url='/login')
def edit_room(request, room_id):
    room=Room.objects.get(id=room_id)
    form=RoomForm(instance=room)
    if request.method == 'POST':
        form=RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            return redirect('/')
    payload={'form':form}
    return render(request, 'base/room_form.html', payload)
    

@login_required(login_url='/login')
def delete_room(request, room_id):
    room = Room.objects.get(id=room_id)
    if request.method == "POST":
        room.delete()
        return redirect('/')

    return render(request, 'base/delete.html',{'obj':room.name})

def logout_page(request):
    logout(request)
    return redirect('/')



