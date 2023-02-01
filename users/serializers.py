from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

from .models import GGCUser, Profile


class UserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        model = GGCUser
        fields = ('id', 'email', 'username', 'password', 'phone_number', 'full_name',)


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = GGCUser
        fields = ('id', 'email', 'username', 'phone_number', 'full_name')


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'user', 'profile_pic', 'get_email', 'get_phone_number', 'get_full_name', 'get_profile_pic', 'get_username']
        read_only_fields = ['user']