from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Dog, Show, Score

def home(request):
    shows = Show.objects.all()
    showw = Show.objects.get(id=1)
    show_dogs = showw.dogs.all()
    dogs = Dog.objects.all()
    scores = Score.objects.all()
    page = 'home'
    context = {'shows': shows, 'dogs': dogs, 'scores': scores, 'show_dogs': show_dogs, 'page': page,}
   
    return render(request, 'base/home.html', context)

def shows(request):
    shows = Show.objects.all()
    page = 'shows'
    context = {
        "shows": shows, "page": page,
    }
    return render(request, 'base/shows.html', context)

def showsDetails(request, pk):
    show = Show.objects.get(id=pk)
    show_dogs = show.dogs.all()
    page = 'shows-details'
    context = {
        "page": page, "show": show, "show_dogs": show_dogs,
    }
    return render(request, 'base/shows_details.html', context)

def loginUser(request):
    page = 'login'
    message = 'git'
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username, password=password)
        except:
            message = "Wrong username or password !"
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    context = {
        "page": page, "message": message,
    }
    return render(request, 'base/login.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def userProfile(request):
    page = 'user-profile'
    context = {
        "page": page,
    }
    return render(request, 'base/user_profile.html', context)



