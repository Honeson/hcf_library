from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.db import models


from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('is_admin', 'is_publisher', 'is_user')


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = UserChangeForm.Meta.fields