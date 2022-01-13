from django import forms
from django.contrib.auth.forms import UserCreationForm

from Account.models import User

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('name','email','password')

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user