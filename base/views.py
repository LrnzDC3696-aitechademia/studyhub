from django.shortcuts import render
from .models import Room


# rooms = [
#     {
#         'id': 1,
#         'name': 'This is room 1',
#         'description': 'This is the description of room 3'
#     },
#     {
#         'id': 2,
#         'name': 'This is room 2',
#         'description': 'This is the description of room 3'
#     },
#     {
#         'id': 3,
#         'name': 'This is room 3',
#         'description': 'This is the description of room 3'
#     }
# ]


def home(request):
    rooms = Room.objects.all()
    context = {
        'rooms': rooms
    }
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    room = Room.objects.get(id=pk)
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context=context)
