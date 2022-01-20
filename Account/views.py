from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from Account.forms import RegistrationForm, LoginForm, AccountUpdationForm
from Account.models import User
# Create your views here.

def account_view(request):
    if not request.user.is_authenticated:
        return render(request,"Account/account.html")
        
    context = {}
    if request.POST:
        email = request.user.email
        form = AccountUpdationForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("account:account")
        else:
            user = User.objects.get(email=email)
            # print(user)
    else:
        user = User.objects.get(email=request.user.email)
        form = AccountUpdationForm(initial={'name':request.user.name,'email':request.user.email})
        
    context['user'] = user
    context['form'] = form
    return render(request,"Account/account.html",context)

def signup_view(request,signup_as):
    # signup_as=""    # when form is invalid, control reaches return render() where signup_as is passed which is not initialised
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)   # dont save it right away, just returns the instance that is gonna get saved
            # if request.POST['as'] == 'vendor':
            if signup_as == '1':
                instance.is_vendor = True
            instance.save()
            
            email = form.cleaned_data.get('email')          # *note
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email,password=raw_password)
            login(request,account)
            return redirect("home")
    else:
        signup_as = signup_as
        form = RegistrationForm()

    return render(request,"Account/signup.html",{'form': form, 'signup_as': signup_as})

def login_view(request,login_as):
    # login_as = ""
    context = {}
    user = request.user

    if user.is_authenticated:
        return redirect("home")
    
    if request.POST:
        form = LoginForm(request.POST)

        if form.is_valid():
            user = User.objects.get(email=form.cleaned_data.get('email'))

            email = request.POST.get('email')
            password = request.POST.get('password')
            # email = request.POST['email']
            # password = request.POST['password'] 
            if (user.is_vendor == True and login_as == '1') or (user.is_vendor == False and login_as == '0'):
                account = authenticate(email=email, password=password)        
                if user:    
                    login(request, account)
                    return redirect("home")
            else:
                return redirect("account:account")
            
    else:
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
