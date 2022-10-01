from django.forms import ModelForm
from .models import Dog, Show, Score, Profile
from django.contrib.auth.models import User

class DogForm(ModelForm):
    class Meta:
        model = Dog
        fields = '__all__'
        exclude = ['owner']

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ['phone']

class ShowForm(ModelForm):
    class Meta:
        model = Show
        fields = ['name','date', 'address', 'description']