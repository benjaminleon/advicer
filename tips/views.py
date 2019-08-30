from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.db.models import Q
from django.shortcuts import redirect
from .models import Movie, Rating
from django.contrib.auth import get_user_model
from tips.getRecommendations import getRecommendations


def index(request):
    User = get_user_model()

    # Extract the relevant information from the models to make the
    # recommendation algorithm agnostic about Django
    users_and_ratings = {}
    users = User.objects.all()
    for user in users:
        ratings = Rating.objects.filter(user = user)

        movies_and_scores = {}
        for rating in ratings:
            movies_and_scores[rating.movie.__str__()] = rating.score

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


def ratings(request):
    choosable_scores = [1, 2, 3, 4, 5]
    context = {
        'ratings': Rating.objects.filter(user = request.user),
        'choosable_scores': choosable_scores,
    }


    return render(request, 'tips/ratings.html', context)


def SetRating(request, movie_id):
    try:
        new_score = request.POST['score']
    except (KeyError):
        return redirect('tips:index')

    print("movie_id: {}".format(movie_id))
    movie = get_object_or_404(Movie, id=movie_id)
    rating, created = Rating.objects.update_or_create(user=request.user, movie=movie)
    if created:
        print("Created a new rating: {}".format(rating))
    else:
        print("Rating existed: {}".format(rating))

    rating.score = new_score
    rating.save()

    return HttpResponseRedirect(reverse('tips:index'))


def UpdateRating(request, rating_id):
    try:
        new_score = request.POST['score']
    except (KeyError):
        return redirect('tips:index')

    print("rating_id: {}".format(rating_id))
    rating = get_object_or_404(Rating, id=rating_id)
    rating.score = new_score
    rating.save()

    return HttpResponseRedirect(reverse('tips:index'))


def DeleteRatingByMovie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rating = Rating.objects.filter(movie=movie, user=request.user)
    rating.delete()
    return HttpResponseRedirect(reverse('tips:index'))


def DeleteRating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    rating.delete()
    return HttpResponseRedirect(reverse('tips:index'))


class SearchResultsView(generic.ListView):
    model = Movie
    template_name = 'tips/search_results.html'

    def get_queryset(self):
        MAX_NR_OF_MOVIES = 20
        query = self.request.GET.get('q')
        matched_movies = Movie.objects.filter(
            Q(title__icontains=query) | Q(release_year__icontains=query))
        matched_movies = matched_movies[:MAX_NR_OF_MOVIES]

        users_ratings = Rating.objects.filter(user=self.request.user)

        object_list = []
        for matched_movie in matched_movies:
            print(f'matched_movie: {matched_movie}')
            rating_found = False
            for rating in users_ratings:
                rating_found = False
                print(rating.movie.__str__())
                if rating.movie.__str__() == matched_movie.__str__():
                    object_list.append({'movie': matched_movie, 'rating': rating})
                    rating_found = True
                    break

            if not rating_found:
                object_list.append({'movie': matched_movie, 'rating': None})

        print(f'object_list: {object_list}')
        MAX_NR_OF_MOVIES_TO_DISPLAY = 20
        return object_list[:MAX_NR_OF_MOVIES_TO_DISPLAY]


    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        context['choosable_scores'] = [1, 2, 3, 4, 5]
        return context