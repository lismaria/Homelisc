from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from Account.forms import RegistrationForm, LoginForm

# Create your views here.

def account_view(request):
    return render(request,"Account/account.html")

def signup_view(request):
    signup_as=""    # when form is invalid, control reaches return render() where signup_as is passed which is not initialised
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)   # dont save it right away, just returns the instance that is gonna get saved
            if request.POST['as'] == 'vendor':
                instance.is_vendor = True
            instance.save()
            
            email = form.cleaned_data.get('email')          # *note
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect("home")
    else:
        signup_as = request.GET['as']
        form = RegistrationForm()

    return render(request,"Account/signup.html",{'form': form, 'signup_as': signup_as})

def login_view(request):
    login_as = ""
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            email = request.POST['email']
            password = request.POST['password']
            account = authenticate(email=email, password=password)
        
            if user:    
                login(request, account)
                return redirect("home")
    else:
        login_as = request.GET['as']
        form = LoginForm()
    context['form'] = form
    context['login_as'] = login_as
    return render(request,"Account/login.html",context)

def logout_view(request):
    logout(request)
    return redirect("account:account")

# *note 
# A Form instance has an is_valid() method, which runs validation routines for all its fields. When this method is called, if all fields contain valid data, it will:
#       return True
#       place the form’s data in its cleaned_data attribute.
