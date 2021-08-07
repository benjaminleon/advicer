from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator


class CustomUser(AbstractUser):
    def __str__(self):
        return self.username


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.title} ({self.release_year})"


class Rating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    score = models.IntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return f"{self.movie.__str__()} got score {self.score}/5 by {self.user}"

    class Meta:
        unique_together = ("movie", "user")
