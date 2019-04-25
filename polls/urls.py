from django.urls import path
from . import views

app_name = 'polls'  # Namespacing
urlpatterns = [
    path('', views.index, name='index'),
    path('vote/<int:new_rating>', views.my_view, name='my_view'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
    path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    path('<int:question_id>/vote/', views.vote, name='vote'),
]
