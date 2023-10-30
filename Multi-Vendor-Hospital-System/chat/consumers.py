import json

from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer

from Doctor.models import Doctor
from Accounts.models import User
from chat.models import Message


class ChatConsumer(WebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.room_name = None
        self.group_name = None
        self.room = None

    def connect(self):
        self.doctor_slug = self.scope["url_route"]["kwargs"]["doctor_slug"]
        self.patient_uuid = self.scope["url_route"]["kwargs"]["patient_uuid"]
        print(self.patient_uuid)

        self.doctor = Doctor.objects.filter(slug=self.doctor_slug).first()
        self.patient = User.objects.filter(uuid=self.patient_uuid).first()
        print(self.doctor)
        print(self.patient)
        if not self.doctor or not self.patient:  # if not appointment also added later
            print("You are not permitted")
            return

        # Group name must be a valid unicode string containing only ASCII alphanumerics, hyphens, or periods.
        self.group_name = f"chat_{self.doctor_slug}_{self.patient_uuid}"

        print(self.group_name)

        # connection has to be accepted
        self.accept()

        # join the room group
        async_to_sync(self.channel_layer.group_add)(
            self.group_name,
            self.channel_name,
        )

        messages = Message.objects.filter(doctor=self.doctor, patient=self.patient)
        msg_list = ""
        for msg in messages:
            msg_list += msg.content
            msg_list += "\n"

        self.send(
            json.dumps(
                {
                    "type": "message_list",
                    "messages": msg_list,
                },
            )
        )

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.group_name,
            self.channel_name,
        )

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        # send chat message event to the room
        async_to_sync(self.channel_layer.group_send)(
            self.group_name,
            {
                "type": "chat_message",
                "message": message,
            },
        )
        Message.objects.create(
            patient=self.patient, doctor=self.doctor, content=message
        )

    def chat_message(self, event):
        self.send(text_data=json.dumps(event))
