from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, 'main_app/index.html')

def register(request):
    errors = User.objects.registrationValidate(request.POST)

    if errors:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        password = request.POST['password']
        dob = request.POST['dob']
        hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt())

        user = User.objects.create( first_name=first_name, last_name = last_name, email = email, password=hashed_pw, dob=dob)
        request.session['user_id'] = user.id
        return redirect('/home')

def home(request):
    return render(request, "main_app/home.html")

def logout(request):
    request.session.clear()
    return redirect('/')