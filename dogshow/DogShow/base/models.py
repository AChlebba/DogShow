
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import User

class Dog(models.Model):
    MALE = 'Male'
    FAMALE = 'Female'
    SEXES = [(MALE,'Male'), (FAMALE,'Female'),]
    name = models.CharField(max_length=100, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    race = models.CharField(max_length=100, null=True)
    sex = models.CharField(max_length=6, choices=SEXES, default=MALE)
    color = models.CharField(max_length=100, default='color')
    birthday = models.DateField(null=True)
    dog_img = models.ImageField(upload_to='static/img', default='img/dog_default.jpg')

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
    active = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)

    class Meta:
        ordering = ['finished', '-date']

    def __str__(self):
        return self.name
    
    @property
    def is_past(self):
        return timezone.now() > self.date

    @property
    def dogs_ready(self):
        if self.dogs.all().count() >= 3:
            return True
        else:
            return False

    @property
    def owners(self):
        dogs = self.dogs.all()
        owners = []
        for dog in dogs:
            owners.append(dog.owner)
        return owners

class Score(models.Model):
    name = models.CharField(max_length=200, blank=False)
    show = models.ForeignKey(Show, on_delete=models.SET_NULL, null=True)
    dog = models.ForeignKey(Dog, on_delete=models.SET_NULL, null=True)
    referee = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    head = models.IntegerField(default=0)
    body = models.IntegerField(default=0)
    legs = models.IntegerField(default=0)
    tail = models.IntegerField(default=0)
    submitted = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.IntegerField(default=000000000, blank=True)
    user_img = models.ImageField(upload_to='static/img', default='img/default_avatar.jpg', blank=True)

class Message(models.Model):
    user = models.TextField(blank=False, max_length=50, default='Guest')
    text = models.TextField(blank=False, max_length=1000)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.text[0:50]
