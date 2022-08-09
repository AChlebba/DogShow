
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Dog(models.Model):
    name = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)

    def __str__(self):
        return self.name

class Show(models.Model):
    name = models.CharField(max_length=200, blank=False)
    date = models.DateTimeField(blank=False)
    address = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    dogs = models.ManyToManyField(Dog, related_name='dogs', blank=True)
    referee1 = models.ForeignKey(User, related_name='referee1', on_delete=models.SET_NULL, null=True)
    referee2 = models.ForeignKey(User, related_name='referee2', on_delete=models.SET_NULL, null=True)
    referee3 = models.ForeignKey(User, related_name='referee3', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.name
    
    @property
    def is_past(self):
        return timezone.now() > self.date

class Score(models.Model):
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True)
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True)
    referee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    head = models.IntegerField(default=0)
    body = models.IntegerField(default=0)
    legs = models.IntegerField(default=0)
    tail = models.IntegerField(default=0)
