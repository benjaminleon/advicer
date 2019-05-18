import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator
from django.conf import settings


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " (" + str(self.release_year) + ")"

    class Meta:
        unique_together = ('title', 'release_year')


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return "{} got score {}/5 by {}".format(self.movie.__str__(), str(self.score), self.user)

    class Meta:
        unique_together = ('movie', 'user')