from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User, Message
from .forms import RoomForm
from django.db.models import Q
# Create your views here.

rooms=None

def login_page(request):
    page='login'
    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        username=request.POST.get('username').lower()
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
    payload={'page':page}
    return render(request, 'base/login_register.html',payload)

def register_page(request):

    if request.user.is_authenticated:
        return redirect('/')

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'User created successfully')
            login(request, user)
            return redirect('/')
        else:
            messages.error(request,'Invalid credentials')
            return redirect('/register')

    form=UserCreationForm()  
    payload = {'form':form}
    return render(request, 'base/login_register.html', payload)

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
    roomMessages=Message.objects.filter(room=room).order_by('-created')
    participants=room.participants.all()
    print(participants)
    if request.method == "POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        return redirect('room',room_id=room.id)

    payload={'room':room, 'roomMessages':roomMessages, 'participants':participants}
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

    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')

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
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')

    if request.method == "POST":
        room.delete()
        return redirect('/')

    return render(request, 'base/delete.html',{'obj':room.name})

def logout_page(request):
    logout(request)
    return redirect('/')



