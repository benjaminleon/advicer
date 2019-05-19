from django.urls import path
from . import views

app_name = 'tips'  # Namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('rate/<int:movie_id>', views.UpdateRating, name='rate'),
    path('deleteRating/<int:movie_id>', views.DeleteRating, name='delete'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
