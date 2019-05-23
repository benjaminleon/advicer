from django.urls import path
from . import views

app_name = 'tips'  # Namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('rate/<int:movie_id>', views.NewRating, name='new_rating'),
    path('updateRating/<int:rating_id>', views.UpdateRating, name='update_rating'),
    path('deleteRating/<int:rating_id>', views.DeleteRating, name='delete'),
    path('deleteRatingByMovie/<int:movie_id>', views.DeleteRatingByMovie, name='deleteByMovie'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
