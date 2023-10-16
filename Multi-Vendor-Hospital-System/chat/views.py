from django.shortcuts import render

# Create your views here.

from django.shortcuts import render


def group_view(request, doctor_id, patient_id):
    # chat_room, created = Room.objects.get_or_create(name=room_name)
    return render(
        request,
        "room.html",
        {
            "room": "Empty",
        },
    )
