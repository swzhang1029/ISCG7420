from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Room

# Create your views here.

@login_required
def room_list(request):
    """View to list all available rooms."""
    rooms = Room.objects.filter(status='available')
    return render(request, 'rooms/room_list.html', {'rooms': rooms})

@login_required
def room_detail(request, room_id):
    """View to show details of a specific room."""
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'rooms/room_detail.html', {'room': room})
