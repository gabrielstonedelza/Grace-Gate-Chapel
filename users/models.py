from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.utils import timezone

User = settings.AUTH_USER_MODEL

class GGCUser(AbstractUser):
    email = models.EmailField(max_length=255)
    full_name = models.CharField(max_length=100, unique=True)
    phone_number = models.CharField(max_length=16, unique=True)
    home_address = models.CharField(max_length=100, blank=True)
    digital_address = models.CharField(max_length=100, blank=True)

    REQUIRED_FIELDS = ['email', 'full_name', 'phone_number','home_address','digital_address']
    USERNAME_FIELD = 'username'

    def get_username(self):
        return self.username

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="d_profile")
    profile_pic = models.ImageField(upload_to="profile_pics", default="default_user.png")

    def __str__(self):
        return self.user.username

    def get_username(self):
        return self.user.username

    def get_email(self):
        return self.user.email

    def get_phone_number(self):
        return self.user.phone_number

    def get_full_name(self):
        return self.user.full_name

    def get_profile_pic(self):
        if self.profile_pic:
            return "http://127.0.0.1:8000" + self.profile_pic.url
        return ''