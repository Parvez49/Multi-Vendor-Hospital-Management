from django.urls import path

from . import views

urlpatterns = [
    path(
        "/<str:doctor_id>/<str:patient_id>/messages", views.group_view, name="chat-room"
    ),
]
