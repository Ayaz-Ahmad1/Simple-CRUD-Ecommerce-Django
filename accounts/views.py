from django.shortcuts import *
from django.contrib.auth.models import User
from core.models import *
from django.contrib.auth import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import Customer

# Create your views here.

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        messages.info(request, "username or password incorrect")
    return render(request, 'accounts/login.html')

def user_register(request):
    if request.method == "POST":
        firstName = request.POST.get('first_name')
        lastName = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        phone = request.POST.get("phone_field")
        
        
    #    print(username, email)
        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already exists")
                return redirect('user_register')
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already exists")
                return redirect('user_register')

            else:
                user = User.objects.create_user(first_name = firstName, last_name = lastName, username=username, email=email, password=password)
                
                profile = Customer(user = user, phone_field = phone)
                user.save()
                profile.save()
                try:
                    if request.FILES["avatar"]:
                        profile.profile_pic = request.FILES["avatar"]
                        user.save()
                        profile.save()
                        messages.info(request, "Profile Created successfully")

                except Exception:
                    messages.info(request, "Profile saved without Profile Image")
                    

                #code for login of user will come here
                our_user = authenticate(username = username, password=password)
                if our_user is not None:
                    login(request, user)
                    return redirect('/')

        else:
            messages.info(request, "Passwords does not match")
            return redirect('user_register')
    return render(request, 'accounts/register.html')


@login_required
def profile (request):
    phone = Customer.objects.get(user = request.user)
    return render(request, 'accounts/profile.html', {"phone":phone})

@login_required
def user_loguot (request):
    logout(request)
    return redirect('/')