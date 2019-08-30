from django.urls import path
from . import views
from django.contrib.auth.decorators import login_required

app_name = 'tips'  # Namespacing
urlpatterns = [
    path('', login_required(views.index, redirect_field_name=None), name='index'),
    path('rate/<int:movie_id>', views.SetRating, name='set_rating'),
    path('updateRating/<int:rating_id>', views.UpdateRating, name='update_rating'),
    path('deleteRating/<int:rating_id>', views.DeleteRating, name='delete'),
    path('deleteRatingByMovie/<int:movie_id>', views.DeleteRatingByMovie, name='deleteByMovie'),
    path('search/', login_required(views.SearchResultsView.as_view(), redirect_field_name=None), name='search_results'),
    path('ratings/', login_required(views.ratings, redirect_field_name=None), name='ratings'),
]
