from django.contrib import admin
from .models import Question
from .models import Movie, MovieRating

# Register your models here.

admin.site.register(Question)
admin.site.register(Movie)
admin.site.register(MovieRating)