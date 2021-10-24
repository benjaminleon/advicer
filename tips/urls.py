from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = "tips"  # Namespacing
urlpatterns = [
    path("", login_required(views.index, redirect_field_name=None), name="index"),
    path("rate/<int:movie_id>", views.set_rating, name="set_rating"),
    path("updateRating/<int:rating_id>", views.update_rating, name="update_rating"),
    path("deleteRating/<int:rating_id>", views.delete_rating, name="delete"),
    path(
        "deleteRatingByMovie/<int:movie_id>",
        views.delete_rating_by_movie,
        name="deleteByMovie",
    ),
    path(
        "search/",
        login_required(views.SearchResultsView.as_view(), redirect_field_name=None),
        name="search_results",
    ),
    path(
        "common/",
        login_required(views.common_movies, redirect_field_name=None),
        name="common",
    ),
    path(
        "ratings/",
        login_required(views.ratings, redirect_field_name=None),
        name="ratings",
    ),
    path(
        "how_it_works/",
        login_required(views.how_it_works, redirect_field_name=None),
        name="how_it_works",
    )
]
