from django import forms
from django.contrib.auth.forms import UserCreationForm

from Account.models import User

class RegistrationForm(forms.ModelForm):
    name = forms.CharField(label='',max_length=32,widget=forms.TextInput(attrs={'placeholder':'Full Name'}))
    email= forms.EmailField(label='',max_length=60,widget=forms.EmailInput(attrs={'placeholder':'Email ID'}))
    password= forms.CharField(label='',max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Choose a password'}))

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