from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from rugby_tipping.models import Tipper

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "username", "password1", "password2")

    def save(self, commit=True):
        user = super(NewUserForm, self).save(commit=False)
        if commit:
            user.save()
        return user
