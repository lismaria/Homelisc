from django import forms
from Account.models import User
from django.contrib.auth import login, authenticate

class RegistrationForm(forms.ModelForm): # ModelForm is used to directly convert a model into a Django form. 

    # name = forms.CharField(label='',max_length=32,widget=forms.TextInput(attrs={'placeholder':'Full Name'}))
    # email= forms.EmailField(label='',max_length=60,widget=forms.EmailInput(attrs={'placeholder':'Email ID'}))
    # password= forms.CharField(label='',max_length=50,widget=forms.PasswordInput(attrs={'placeholder':'Choose a password'}))

    class Meta:
        model = User
        fields = ('name','email','password')
        labels = {
            'name': '',
            'email': '',
            'password': '',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder':'Full Name'}),
            'email': forms.EmailInput(attrs={'placeholder':'Email ID'}),
            'password': forms.PasswordInput(attrs={'placeholder':'Choose a password'})
        }

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('email', 'password') 
        labels = {
            'email': '',
            'password': '',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':'Email ID', 'ng-model':'email', 'ng-required':'true',}),
            'password': forms.PasswordInput(attrs={'placeholder':'Password','ng-model':'password', 'ng-required':'true', 'ng-minlength':'8'})
        }

    def clean(self):    # available to any form that extends the ModelForm. It runs before the form can do anything
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Incorrect Email ID or Password")


class AccountUpdationForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('profile_pic','name','email')
        labels = {
            'profile_pic':'',
            'name': 'Name :',
            'email': 'Email :',
        }
        widgets = {
            'profile_pic': forms.FileInput(attrs={"id":"change_pic","style":"display:none","onchange":"document.getElementById('dp').src = window.URL.createObjectURL(this.files[0])","accept":"image/png, image/jpeg"}),
            'name': forms.TextInput(attrs={"onfocus":"input_focus()","onblur":"input_blur()", 'ng-required':'true',}),
            'email': forms.EmailInput(attrs={"onfocus":"input_focus()","onblur":"input_blur()",'ng-model':'email', 'ng-required':'true',}),
        }

    def clean_email(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            try:
                account = User.objects.exclude(pk=self.instance.pk).get(email=email)    # To get the primary key of the user
            except User.DoesNotExist:
                return email
            raise forms.ValidationError("Email is already in use.")
