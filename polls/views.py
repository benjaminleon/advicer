from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib.auth.models import User

from .models import Choice, Question
from .models import Movie, Rating

from polls.getRecommendations import getRecommendations

def index(request):
    if not request.user.is_authenticated:
        return render(request, 'polls/index.html')

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

    return render(request, 'polls/index.html', context)


class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'

    def get_queryset(self):
        """
        Excludes any questions that aren't published yet.
        """
        return Question.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'


def UpdateRating(request, new_rating):
    ratings = list(Rating.objects.filter(user = request.user, movie = 5))
    print("\n")
    for rating in ratings:
        print(rating)
        rating.rating = new_rating
        rating.save()

    print(rating)
    print("\n")
    print("I will do useful things in the future!")

    return HttpResponseRedirect(reverse('polls:index'))


def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
            # Redisplay the question voting form.
            return render(request, 'polls/detail.html', {
                'question': question,
                'error_message': "You didn't select a choice dude.",
            })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
