from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, User, Message
from .forms import RoomForm, UserForm
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
    topics=Topic.objects.all()[0:5]
    count=rooms.count()
    if params:
        room_messages=Message.objects.all().order_by('-created').filter(Q(room__topic__name__icontains=params))
    else:
        room_messages=Message.objects.all().order_by('-created')

    payload={'rooms':rooms, 'topics':topics,'room_count':count, 'room_messages':room_messages}
    
    return render(request, 'base/home.html', payload)


def room(request, room_id):
    
    room=Room.objects.get(id=room_id)
    roomMessages=Message.objects.filter(room=room).order_by('-created')
    participants=room.participants.all()

    if request.method == "POST":
        message=Message.objects.create(
            user=request.user,
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        print(room.participants)
        return redirect('room',room_id=room.id)

    payload={'room':room, 'roomMessages':roomMessages, 'participants':participants}
    return render(request, 'base/room.html', payload)

def userProfile(request, user_id):
    user=User.objects.get(id=user_id)
    rooms=Room.objects.filter(host=user)
    room_messages=Message.objects.filter(user=user)
    topics=Topic.objects.all()
    payload={'user':user, 'rooms':rooms, 'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', payload)

@login_required(login_url='/login')
def updateUser(request):
    form=UserForm(instance=request.user)

    if request.method == 'POST':
        form=UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request,'User updated successfully')
            return redirect('user-profile', user_id=request.user.id)
        
    return render(request,'base/update-user.html', {'form':form})

@login_required(login_url='/login')
def create_room(request):
    form=RoomForm()
    topics=Topic.objects.all()
    if request.method == 'POST':
        topic_name=request.POST.get('topic')
        topic,created = Topic.objects.get_or_create(name=topic_name)
        print(request.POST)
        Room.objects.create(
            host=request.user,
            topic=topic,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        return redirect('/')
        
    payload={'form':form, 'topics':topics}
    return render(request, 'base/room_form.html', payload)


@login_required(login_url='/login')
def edit_room(request, room_id):
    room=Room.objects.get(id=room_id)
    form=RoomForm(instance=room)
    topics=Topic.objects.all()
    if request.user != room.host:
        return HttpResponse('You are not authorized to edit this room')

    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name=request.POST.get('name')
        room.topic=topic
        room.description=request.POST.get('description')
        room.save()
        return redirect('/')
    payload={'form':form, 'topics':topics, 'room':room}
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

@login_required(login_url='/login')
def delete_message(request, message_id):
    message = Message.objects.get(id=message_id)

    if request.user != message.user:
        return HttpResponse('You are not authorized to delete this message')

    if request.method == "POST":
        message.delete()
        return redirect('room', room_id=message.room.id)

    return render(request, 'base/delete.html',{'obj':message.body})
 
def topicsPage(request):
    params = request.GET.get('q') if request.GET.get('q') else ''
    topics=Topic.objects.filter(name__icontains=params)
    payload={'topics':topics}
    return render(request, 'base/topics.html',payload)

def logout_page(request):
    logout(request)
    return redirect('/')



