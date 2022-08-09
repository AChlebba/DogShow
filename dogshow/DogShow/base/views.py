
import re
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Dog, Show, Score
from .forms import DogForm, ShowForm

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
    message = ''
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

def registerUser(request):
    message = ''
    form = UserCreationForm
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
        else:
            message = 'Something wnet wrong :/'
    context = {
        "form": form, "message": message,
    }
    return render(request, 'base/register.html', context)

def userProfile(request):
    page = 'user-profile'
    dogs = Dog.objects.all()
    context = {
        "page": page, "dogs":dogs,
    }
    return render(request, 'base/user_profile.html', context)

def newDog(request):
    message = ''
    form = DogForm
    if request.method == 'POST':
        form = DogForm(request.POST)
        if form.is_valid():
            dog = form.save(commit=False)
            dog.owner = request.user
            dog.save()
            return redirect('user-profile')
        else:
            message = 'Date in format year-month-day (2001-01-01)'
    context = {
        "form": form, "message": message,
    }
    return render(request, 'base/new_dog.html', context)

def deleteDog(request, pk):
    dog = Dog.objects.get(id=pk)
    if request.user == dog.owner:
        dog.delete()
        page = 'user-profile'
        dogs = Dog.objects.all()
        return redirect('user-profile')
    else:
        message = 'jakas lipa wyszla'

def dogProfile(request, pk):
    dog = Dog.objects.get(id=pk)
    context = {
        "dog": dog
        }
    return render(request, 'base/dog_profile.html', context)

def submitDog(request, pk):
    message = ''
    dogs = Dog.objects.all()
    show = Show.objects.get(id=pk)
    show_dogs = show.dogs.all()
    if request.method == 'POST':
        try:
            dog = request.POST.get('selected-dog')
            show.dogs.add(dog)
            return redirect('shows')
        except:
            message = 'Choose a dog'

    context = {
        "message": message, "dogs": dogs, "show": show, "show_dogs": show_dogs,
    }
    return render(request, 'base/submit_dog.html', context)

def cancelDog(request, pk, dpk):
    dog = Dog.objects.get(id=dpk)
    show = Show.objects.get(id=pk)
    
    if request.user == dog.owner:
        show.dogs.remove(dog)
        return redirect('shows')
    else:
        message = 'jakas lipa wyszla'


def addShow(request):
    page = 'add_show'
    form = ShowForm
    message = ''

    if request.method == 'POST':
        form = ShowForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('shows')
        else:
            message = 'Date in format year-month-day (2006-10-25 14:30)'

    context = {
        "page": page, "form": form, "message": message,
    }
    return render(request, 'base/add_show.html', context)


def addReferee(request, pk, rpk):
    show = Show.objects.get(id=pk)
    referees = Group.objects.get(name='referee').user_set.all()
    message = ''
    referee_dict = {
        "1": show.referee1, "2": show.referee2, "3": show.referee3,
    }

    if request.method == 'POST':
        try:
            referee = request.POST.get('selected-referee')
            referee = User.objects.get(id=referee)
            if rpk == '1':
                show.referee1 = referee
            if rpk == '2':
                show.referee2 = referee
            if rpk == '3':
                show.referee3 = referee
            show.save()
            return redirect('shows')
        except:
            message = referee

    context = {
        "referees": referees, "show": show, "message": message,
    }
    return render(request, 'base/add_referee.html', context)




