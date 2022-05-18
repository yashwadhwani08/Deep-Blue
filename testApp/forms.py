from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import User


class TestUserCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('email',)


class TestUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email','phone')