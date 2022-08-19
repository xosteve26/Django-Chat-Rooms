from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room
from .forms import RoomForm
# Create your views here.

rooms=None

def home(request):
    rooms=Room.objects.all()
    payload={'rooms':rooms}
    
    return render(request, 'base/home.html', payload)


def room(request, room_id):
    room=Room.objects.get(id=room_id)
    payload={'room':room}
    return render(request, 'base/room.html', payload)


def create_room(request):
    form=RoomForm()
    if request.method == 'POST':
        form=RoomForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    payload={'form':form}
    return render(request, 'base/room_form.html', payload)

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