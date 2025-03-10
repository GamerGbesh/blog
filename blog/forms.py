from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUser(UserCreationForm):
    class Meta:
        model = User
        fields = ["username", "password1", "password2"]

    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = user.username.lower()
        if commit:
            user.save()
        return user