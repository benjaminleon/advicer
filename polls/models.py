import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

# Create your models here.

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        now = timezone.now()
        yesterday = now - datetime.timedelta(days=1)
        return yesterday <= self.pub_date <= now


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text


class Movie(models.Model):
    title = models.CharField(max_length=200)
    release_year = models.IntegerField(default=0)

    def __str__(self):
        return self.title + " (" + str(self.release_year) + ")"

    class Meta:
        unique_together = ('title', 'release_year')


class UserRating(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)
    user_name = models.CharField(max_length=200)
    rating = models.IntegerField(default=0, validators=[MaxValueValidator(5)])

    def __str__(self):
        return "{} got score {}/5 by {}".format(self.movie.__str__(), str(self.rating), self.user_name)

    class Meta:
        unique_together = ('movie', 'user_name')