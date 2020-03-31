from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.views import generic
from django.utils import timezone

from .models import Question
# Create your views here.

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """
        Return the last five published questions (not including those set to be
        published in the future).
        """
        return Question.objects.filter(
        pub_date__lte=timezone.now()
        )

class DetailView(generic.DetailView):
    model = Question
    template = 'polls/detail.html'

class ResultView(generic.DetailView):
    model = Question
    template = 'polls/results.html'

"""We’re using two generic views here: ListView and DetailView. Respectively,
those two views abstract the concepts of “display a list of objects” and “display a
detail page for a particular type of object.”
    1.Each generic view needs to know what model it will be acting upon. This is provided
    using the model attribute.
    2. The DetailView generic view expects the primary key value captured from the URL
    to be called "pk", so we’ve changed question_id to pk for the generic views.

For DetailView the question variable is provided automatically – since we’re using
a Django model (Question), Django is able to determine an appropriate name for the
context variable.
"""

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the question voting form.
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))
