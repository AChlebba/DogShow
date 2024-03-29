
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from .models import Dog, Show, Score, Message
from .forms import DogForm, ShowForm, ProfileForm
from django.http import HttpResponse
import requests


def home(request):
    page = 'home'
    context = {
        "page": page,
        }
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
    score_cards = list(Score.objects.filter(show=show))
    all_finished = False
    if score_cards and not show.finished:
        for score in score_cards:
            if score.submitted:
                all_finished = True
            else:
                all_finished = False
                break

    if all_finished and not show.finished:
        show.finished = True
        show.active = False
        show.save()

    if show.finished and show.active:
        show.active = False
        show.save()

    show_dogs = show.dogs.all()
    show_dogs_number = show.dogs.count()
    dog_points = {}
    if show.finished:
        dog_names = []
        for dog in show_dogs:
            if dog.name not in dog_names:
                dog_names.append([dog.name,0,0,0,0,0])
        dog_points = {item[0]: item[1:] for item in dog_names}
        for score in score_cards:
            if score.dog == None:
                continue
            dog_points[score.dog.name][0] += score.head
            dog_points[score.dog.name][1] += score.body
            dog_points[score.dog.name][2] += score.legs
            dog_points[score.dog.name][3] += score.tail
            dog_points[score.dog.name][4] += (score.head + score.body + score.legs + score.tail)
        dog_points = dict(sorted(dog_points.items(), key=lambda item: item[1][4], reverse=True))
    
    page = 'shows-details'
    context = {
        "page": page, "show": show, "show_dogs": show_dogs, "score_cards": score_cards, "all_finished": all_finished, "dog_points": dog_points, "show_dogs_number": show_dogs_number,
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
    user_form = UserCreationForm
    profile_form = ProfileForm
    if request.method == 'POST':
        user_form = UserCreationForm(request.POST, request.FILES)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            name = user.username

            response = requests.get(f"https://avatars.dicebear.com/api/male/{name}.svg")
            with open(f"static/img/avatar{name}.svg", "wb") as file:
                file.write(response.content)
            profile_form.instance.user_img = (f"img/avatar{name}.svg")
            profile_form.instance.user = user
            profile_form.save()
            
            login(request, user)
            return redirect('home')
        else:
            message = 'Something wnet wrong :/'
    context = {
        "user_form": user_form, "profile_form": profile_form, "message": message,
    }
    return render(request, 'base/register.html', context)


@login_required
def userProfile(request):
    page = 'user-profile'
    dogs = Dog.objects.all()
    context = {
        "page": page, "dogs": dogs,
    }
    return render(request, 'base/user_profile.html', context)


@login_required
def newDog(request):
    message = ''
    form = DogForm
    if request.method == 'POST':
        form = DogForm(request.POST, request.FILES)
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


@login_required
def deleteDog(request, pk):
    dog = Dog.objects.get(id=pk)
    if request.user == dog.owner:
        dog.delete()
        scores = Score.objects.filter(dog=dog, submitted=False)
        scores.delete()
        return redirect('user-profile')
    else:
        return redirect('home')


def dogProfile(request, pk):
    dog = Dog.objects.get(id=pk)
    shows = list(Show.objects.filter(dogs = dog))
    context = {
        "dog": dog, "shows": shows,
        }
    return render(request, 'base/dog_profile.html', context)


@login_required
def submitDog(request, pk):
    message = ''
    dogs = Dog.objects.all()
    show = Show.objects.get(id=pk)
    if show.active or show.finished:
        return redirect('shows')
    show_dogs = show.dogs.all()

    if request.method == 'POST':
        try:
            dog = request.POST.get('selected-dog')
            show.dogs.add(dog)
            return redirect('shows-details', pk)
        except:
            message = 'Choose a dog'

    context = {
        "message": message, "dogs": dogs, "show": show, "show_dogs": show_dogs,
    }
    return render(request, 'base/submit_dog.html', context)


@login_required
def cancelDog(request, pk, dpk):
    dog = Dog.objects.get(id=dpk)
    show = Show.objects.get(id=pk)
    
    if request.user == dog.owner:
        show.dogs.remove(dog)
        return redirect('shows-details', pk)
    else:
        return redirect('login')


@login_required
def addShow(request):
    if not request.user.groups.filter(name='admin').exists():
        return redirect('login')

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


@login_required
def addReferee(request, pk, rpk):
    if not request.user.groups.filter(name='admin').exists():
        return redirect('login')

    show = Show.objects.get(id=pk)
    show_dogs = show.dogs.all()
    if show.active or show.finished:
        return redirect('shows')
    referees = Group.objects.get(name='referee').user_set.all()
    message = ''

    if request.method == 'POST':
        try:
            referee = request.POST.get('selected-referee')
            if referee == '---':
                if rpk == '1':
                    show.referee1 = None
                if rpk == '2':
                    show.referee2 = None
                if rpk == '3':
                    show.referee3 = None
                show.save()
                return redirect('shows-details', pk)
            else:
                referee = User.objects.get(id=referee)
                if rpk == '1':
                    show.referee1 = referee
                if rpk == '2':
                    show.referee2 = referee
                if rpk == '3':
                    show.referee3 = referee
                show.save()
                return redirect('shows-details', pk)
        except:
            message = referee

    context = {
        "referees": referees, "show": show, "show_dogs": show_dogs, "message": message,
    }
    return render(request, 'base/add_referee.html', context)


@login_required
def activateShow(request, pk):
    if not request.user.groups.filter(name='admin').exists():
        return redirect('shows')
    else:
        current_show = Show.objects.get(id=pk)
        if current_show.active:
            scores = Score.objects.all()
            for score in scores:
                if score.show == current_show:
                    score.delete()
            current_show.active = False
            current_show.save()
            return redirect('shows-details', pk)
        else:
            if current_show.finished:
                return redirect('shows')
            if Score.objects.filter(show=current_show).exists():
                current_show.active = True
                current_show.save()
                return redirect('shows-details', pk)
            else:
                for dog in current_show.dogs.all():
                    score = Score.objects.create(
                        name = current_show.name + ' ' + current_show.referee1.username + ' ' + dog.name,
                        show = current_show,
                        referee = current_show.referee1,
                        dog = dog)
                    score.save()
                for dog in current_show.dogs.all():
                    score = Score.objects.create(
                        name = current_show.name + ' ' + current_show.referee2.username + ' ' + dog.name,
                        show = current_show,
                        referee = current_show.referee2,
                        dog = dog)
                    score.save()
                for dog in current_show.dogs.all():
                    score = Score.objects.create(
                        name = current_show.name + ' ' + current_show.referee3.username + ' ' + dog.name,
                        show = current_show,
                        referee = current_show.referee3,
                        dog = dog)
                    score.save()

                current_show.active = True
                current_show.save()
                return redirect('shows-details', pk)


@login_required
def scorePage(request, pk, dpk):
    if not request.user.groups.filter(name='referee').exists():
        return redirect('login')

    show = Show.objects.get(id=pk)
    dogs = show.dogs.all()
    scores = Score.objects.all()
    dogs_count = len(dogs)-1
    not_finished = scores.filter(show=show, referee=request.user, submitted=False).exists()
    if int(dpk) not in range(dogs_count+1):
        dpk = 0

    for i, dog in enumerate(dogs):
        if i == int(dpk):
            current_dog = dog
            break

    score = scores.get(show=show, dog=dog, referee=request.user)
    
    if request.method == 'POST':
        if show.finished or not show.active:
            return redirect('shows')
        score.head = request.POST.get('head')
        score.body = request.POST.get('body')
        score.legs = request.POST.get('legs')
        score.tail = request.POST.get('tail')
        score.submitted = True
        score.save()
        not_finished = scores.filter(show=show, referee=request.user, submitted=False).exists()

    context = {
        "show": show, "current_dog": current_dog, "score": score, "dogs_count": dogs_count, "dpk": dpk, "not_finished": not_finished,
    }
    return render(request, 'base/score_page.html', context)


@login_required
def refereeList(request):
    if not request.user.groups.filter(name='admin').exists():
        return redirect('login')

    referees = User.objects.all()
    page = 'referees'
    context = {
        "referees": referees, "page": page,
    }
    return render(request, 'base/referee_list.html', context)


@login_required
def refereeOnOff(request, pk):
    if request.user.groups.filter(name='admin').exists():
        referee = User.objects.get(id=pk)
        group = Group.objects.get(name='referee')
        if referee.groups.filter(name='referee').exists():
            shows = Show.objects.all()
            for show in shows:
                if show.active or show.finished:
                    continue
                else:
                    if show.referee1 == referee:
                        show.referee1 = None
                    if show.referee2 == referee:
                        show.referee2 = None
                    if show.referee3 == referee:
                        show.referee3 = None
                show.save()
            referee.groups.remove(group)
        else:
            referee.groups.add(group)
    else:
        return redirect('shows')

    return redirect('referee-list')


def chat(request):
    page = 'chat'
    messages = Message.objects.all().order_by('created')
    if request.method == 'POST':
        if len(request.POST.get('newMessage').strip()) == 0:
            return redirect('chat')
        if len(request.POST.get('newMessage')) > 999:
            return redirect('chat')
        if request.user.is_authenticated:
            message = Message.objects.create(
                user = request.user.username,
                text = request.POST.get('newMessage')
            )
        else:
             message = Message.objects.create(
                user = "Guest",
                text = request.POST.get('newMessage')
            )
        message.save()
        return HttpResponse(status=204)
    context = {
        "page": page, "messages": messages
    }
    return render(request, 'base/chat.html', context)


def chatRefresh(request):
    page = 'chat'
    messages = Message.objects.all().order_by('created')
    context = {
        "page": page, "messages": messages
    }
    return render(request, 'base/chat_refresh.html', context)


def api(request):
    page = 'api'
    context = {
        "page": page,
    }
    return render(request, 'base/api.html', context)


def dogs(request):
    page = 'dogs'
    response = requests.get("http://127.0.0.1:8000/api/dog-list/")
    data = response.json()
    context = {
        "page": page, "data": data,
    }
    return render(request, 'base/dogs.html', context)