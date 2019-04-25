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
    if not request.user.get_username():
        return render(request, 'polls/index.html')

    current_user_name = request.user.get_username

    current_users_ratings = [rating for rating in Rating.objects.filter(user = request.user)]
    other_users_ratings = [rating for rating in Rating.objects.all().exclude(user = request.user)]

    other_users_names = [user.get_username() for user in User.objects.all() if user.get_username != current_user_name]

    other_users_and_ratings = {}

    for name in other_users_names:
        other_users_and_ratings[name] = [rating for rating in other_users_ratings if rating.user.get_username() == name]

    recommendations = getRecommendations(current_users_ratings, other_users_and_ratings)

    context = {
        'movies': Movie.objects.all(),
        'ratings': Rating.objects.all(),
        'recommendations': recommendations,
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


def my_view(request):
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
