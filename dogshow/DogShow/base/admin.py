from django.contrib import admin

from .models import Dog, Show, Score, Profile
admin.site.register(Dog)
admin.site.register(Show)
admin.site.register(Score)
admin.site.register(Profile)
