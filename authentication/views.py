from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from org import settings


# Create your views here.

def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get("username")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        pass1 = request.POST.get("pass1")
        pass2 = request.POST.get("pass2")

        if User.objects.filter(username=username):
            messages.error(request, "Username already exist !! Please try some other username")
            return redirect('home')

        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters.")

        if pass1 != pass2:
            messages.error(request, "Password didn't match!!")

        if not username.isalnum():
            messages.error(request, "Username must be Alpha-Numerical..!")
            return redirect("home")


        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()

        messages.success(request, "your account successfully created...")

        # welcome email
        subject = "welcome to org - Django Login.."
        message = "Hello" + myuser.first_name + "!! \n Thank you for visiting our website \n We have also sent you a confirmation email, please confirm email address in order to activate your account .. \n\n Thanking You \n "
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject, message, from_email, to_list, fail_silently=True)

        return redirect("signin")
    return render(request, "authentication/signup.html")

def signin(request):
    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            fname = user.first_name
            return render(request,  "authentication/index.html", {'fname':fname})
        else:
            messages.error(request, "Bad Credential..")
            return redirect('home')
    return render(request, "authentication/signin.html")

def signout(request):
    logout(request)
    messages.success(request,"logged out successfully..")
    return redirect("home")
