from django.shortcuts import render
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

