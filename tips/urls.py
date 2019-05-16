from django.urls import path
from . import views

app_name = 'tips'  # Namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:new_rating>', views.UpdateRating, name='update_rating'),
    path('search/', views.SearchResultsView.as_view(), name='search_results'),
]
