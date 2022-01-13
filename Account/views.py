from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth import login,authenticate
from Account.forms import RegistrationForm

# Create your views here.

def account_view(request):
    return render(request,"Account/account.html")

def signup_view(request):
    signup_as=""
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)   # dont save it right away, just returns the instance that is gonna get saved
            if request.POST['as'] == 'vendor':
                instance.is_vendor = True
            instance.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect("home")
    else:
        signup_as = request.GET['as']
        form = RegistrationForm()

    return render(request,"Account/signup.html",{'form':form,'signup_as':signup_as})

def login_view(request):
    login_as = request.GET['as']
    return render(request,"Account/login.html",{'login_as':login_as})