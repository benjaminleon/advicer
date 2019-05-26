from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser, Movie, Rating

class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = get_user_model()#CustomUser
    list_display = ['email', 'username',]

admin.site.register(get_user_model(), CustomUserAdmin)
admin.site.register(Movie)
admin.site.register(Rating)