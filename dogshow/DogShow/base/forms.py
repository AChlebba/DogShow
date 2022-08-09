from django.forms import ModelForm
from .models import Dog, Show, Score
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

class ShowForm(ModelForm):
    class Meta:
        model = Show
        fields = ['name','date', 'address', 'description']