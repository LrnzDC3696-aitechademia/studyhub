from django.shortcuts import render


rooms = [
    {
        'id': 1,
        'name': 'This is room 1'
    },
    {
        'id': 2,
        'name': 'This is room 2'
    },
    {
        'id': 3,
        'name': 'This is room 3'
    }
]


def home(request):
    context = {
        'rooms': rooms
    }
    return render(request, 'base/home.html', context=context)


def room(request, pk):
    room = None
    for i in rooms:
        if i['id'] == int(pk):
            room = i
            break
    context = {
        'room': room
    }
    return render(request, 'base/room.html', context=context)
