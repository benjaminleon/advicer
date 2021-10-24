import requests
from bs4 import BeautifulSoup
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.db.models import Q
from django.shortcuts import redirect
from .models import Movie, Rating
from django.contrib.auth import get_user_model
from tips.get_recommendations import get_recommendations
import re

MAX_NR_OF_RESULTS = 5
CHOOSABLE_SCORES = [1, 2, 3, 4, 5]


def index(request):
    user = get_user_model()

    users_and_ratings = {}
    users = user.objects.all()
    for user in users:
        ratings = Rating.objects.filter(user=user)

        movies_and_scores = {}
        for rating in ratings:
            movies_and_scores[rating.movie.__str__()] = rating.score

        users_and_ratings[user.get_username()] = movies_and_scores

    current_user_name = request.user.get_username()
    rec_titles_and_years = get_recommendations(current_user_name, users_and_ratings)

    rec_titles = []
    rec_release_years = []
    for rec_title_and_release_year in rec_titles_and_years:
        m = re.search(r"(.*) \((\d+)\)", rec_title_and_release_year)
        rec_titles.append(m.group(1))
        rec_release_years.append(m.group(2))

    rec_movies = Movie.objects.filter(
        Q(title__in=rec_titles, release_year__in=rec_release_years)
    )

    context = {
        "recommendations": rec_movies,
        "choosable_scores": CHOOSABLE_SCORES,
    }

    return render(request, "tips/index.html", context)


def common_movies(request):
    ratings = Rating.objects.all()
    rating_count = {}
    for rating in ratings:
        if rating.movie in rating_count:
            rating_count[rating.movie] += 1
        else:
            rating_count[rating.movie] = 1

    sorted_common_movies = sorted(rating_count, key=rating_count.get, reverse=True)

    users_ratings = Rating.objects.filter(user=request.user)
    users_movies = [rating.movie for rating in users_ratings]

    already_seen = set(sorted_common_movies) & set(users_movies)

    for seen in already_seen:
        sorted_common_movies.remove(seen)

    context = {
        "common_movies": sorted_common_movies,
        "choosable_scores": CHOOSABLE_SCORES,
    }

    return render(request, "tips/common_movies.html", context)


def ratings(request):
    context = {
        "ratings": Rating.objects.filter(user=request.user),
        "choosable_scores": CHOOSABLE_SCORES,
    }

    return render(request, "tips/ratings.html", context)


def set_rating(request, movie_id):
    try:
        new_score = request.POST["score"]
    except KeyError:
        return redirect("tips:index")

    print(f"movie_id: {movie_id}")
    movie = get_object_or_404(Movie, id=movie_id)
    print(f"movie: {movie}")
    rating, created = Rating.objects.update_or_create(user=request.user, movie=movie)
    if created:
        print(f"Created a new rating: {rating}")
    else:
        print(f"Rating existed: {rating}")

    rating.score = new_score
    rating.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def update_rating(request, rating_id):
    try:
        new_score = request.POST["score"]
    except KeyError:
        return redirect("tips:index")

    print(f"rating_id: {rating_id}")
    rating = get_object_or_404(Rating, id=rating_id)
    rating.score = new_score
    rating.save()

    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


def delete_rating_by_movie(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    rating = Rating.objects.filter(movie=movie, user=request.user)
    rating.delete()
    return HttpResponseRedirect(reverse("tips:index"))


def delete_rating(request, rating_id):
    rating = get_object_or_404(Rating, id=rating_id)
    rating.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


class SearchResultsView(generic.ListView):
    model = Movie
    template_name = "tips/search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        matched_movies = Movie.objects.filter(Q(title__in=[query]))
        if not matched_movies:
            matched_movies = Movie.objects.filter(Q(title__icontains=query))
        matched_movies = matched_movies[:MAX_NR_OF_RESULTS]
        print(matched_movies)
        users_ratings = Rating.objects.filter(user=self.request.user)

        object_list = []
        for matched_movie in matched_movies:
            print(f"matched_movie: {matched_movie}, {matched_movie.img_link}, {matched_movie.id}")
            if matched_movie.img_link == "_":
                print("Gonna find the url to the image")

                r = requests.get(f'https://www.imdb.com/title/{matched_movie.imdb_id}')
                if r:
                    soup = BeautifulSoup(r.text, 'html.parser')
                    if soup:
                        url = soup.img['src']
                        if url.startswith("//fls"):
                            print(f"Only got a pixel for {matched_movie.imdb_id}: {url}")
                            m = get_object_or_404(Movie, id=matched_movie.id)
                            m.img_link = "failed"
                            print("adding 'failed' to database for the movie")
                            m.save()
                        else:
                            print(f"url: {url}")
                            matched_movie.img_link = url
                            m = get_object_or_404(Movie, id=matched_movie.id)
                            m.img_link = url
                            print("adding url to database")
                            m.save()

                    else:
                        print("no soup")
                else:
                    print(f"no response for https://www.imdb.com/title/{matched_movie.id}")

            rating_found = False
            for rating in users_ratings:
                rating_found = False
                if rating.movie.__str__() == matched_movie.__str__():
                    object_list.append({"movie": matched_movie, "rating": rating})
                    rating_found = True
                    break

            if not rating_found:
                object_list.append({"movie": matched_movie, "rating": None})

        print(f"object_list: {object_list}")
        return object_list[:MAX_NR_OF_RESULTS]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["choosable_scores"] = CHOOSABLE_SCORES
        return context
