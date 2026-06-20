from django.contrib.auth import get_user_model
from rest_framework import serializers

from .models import Profile

User = get_user_model()


class GoogleAuthSerializer(serializers.Serializer):
    id_token = serializers.CharField(write_only=True)


class ProfileSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(source="user.email", read_only=True)
    capabilities = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ["email", "display_name", "capabilities", "phone", "avatar_url", "birthday"]
        read_only_fields = ["capabilities"]

    def get_capabilities(self, obj):
        return {"leasing": obj.leasing_capabilities()}
