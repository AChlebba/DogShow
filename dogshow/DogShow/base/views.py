from django.shortcuts import render
from .models import Dog, Show, Score

def home(request):
    shows = Show.objects.all()
    showw = Show.objects.get(id=1)
    show_dogs = showw.dogs.all()
    dogs = Dog.objects.all()
    scores = Score.objects.all()

    context = {'shows': shows, 'dogs': dogs, 'scores': scores, 'show_dogs': show_dogs }
   
    return render(request, 'base/home.html', context)

