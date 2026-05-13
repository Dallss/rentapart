from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(write_only=True)


class SetRoleSerializer(serializers.Serializer):
    role = serializers.ChoiceField(
        choices=[
            (Profile.Role.LANDLORD.value, Profile.Role.LANDLORD.label),
            (Profile.Role.RENTER.value, Profile.Role.RENTER.label),
        ],
    )


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Profile
        fields = ["email", "username", "role", "phone", "bio", "avatar"]
        read_only_fields = ["role"]
