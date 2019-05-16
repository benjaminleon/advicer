from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models import Q

from .models import Movie, Rating

from tips.getRecommendations import getRecommendations

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'tips/index.html')

    # Extract the relevant information from the models to make the
    # recommendation algorithm agnostic about Django
    users_and_ratings = {}
    users = User.objects.all()
    for user in users:
        ratings = Rating.objects.filter(user = user)

        movies_and_scores = {}
        for rating in ratings:
            movies_and_scores[rating.movie.__str__()] = rating.rating

        users_and_ratings[user.get_username()] = movies_and_scores

    current_user_name = request.user.get_username()
    recommendations = getRecommendations(current_user_name, users_and_ratings)

    choosable_scores = [1, 2, 3, 4, 5]
    context = {
        'movies': Movie.objects.all(),
        'ratings': Rating.objects.all(),
        'recommendations': recommendations,
        'choosable_scores': choosable_scores,
    }

    return render(request, 'tips/index.html', context)


def UpdateRating(request, new_rating):
    ratings = list(Rating.objects.filter(user = request.user, movie = 5))
    print("\n")
    for rating in ratings:
        print(rating)
        rating.rating = new_rating
        rating.save()

    print("\n")
    print("I will do useful things in the future!")

    return HttpResponseRedirect(reverse('tips:index'))
    

class SearchResultsView(generic.ListView):
    model = Movie
    template_name = 'tips/search_results.html'

    def get_queryset(self):
        query = self.request.GET.get('q')
        object_list = Movie.objects.filter(
            Q(title__icontains=query) | Q(release_year__icontains=query))
        return object_list