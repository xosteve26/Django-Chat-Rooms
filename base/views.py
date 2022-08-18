from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
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
