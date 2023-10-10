from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import User, BloodGroups, Notification
from .email_validation import email_validation


class NotificationDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("uuid", "notification_head", "content")


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ("uuid", "notification_head", "is_read")

    def create(self, validated_data):
        user_uuid = validated_data["recipient"]
        user = User.objects.filter(uuid=user_uuid).first()
        validated_data["recipient"] = user
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, style={"input_type": "password"})

    def create(self, validated_data):
        user = User.objects.create(email=validated_data["email"])
        user.set_password(validated_data["password"])
        user.save()
        return user


# from .models import User


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = "__all__"


class PhoneNumberSerializerField(serializers.CharField):
    def to_representation(self, obj):
        return str(obj)

    def to_internal_value(self, data):
        return data


class PublicUserListSerializer(serializers.ModelSerializer):
    blood_group = serializers.ChoiceField(choices=BloodGroups.choices)
    contact_number = PhoneNumberSerializerField()
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "uuid",
            "first_name",
            "last_name",
            "gender",
            "date_of_birth",
            "height",
            "weight",
            "blood_group",
            "nationality",
            "email",
            "password",
            "contact_number",
            "profile_picture",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        password = validated_data.pop("password")
        email = validated_data.pop("email")  # Include email in the validated_data
        # if not email_validation(email):
        #    raise serializers.ValidationError("Invalid or Inactive email!")
        user = User(email=email, **validated_data)
        user.set_password(password)
        user.is_active = False
        user.save()
        return user
