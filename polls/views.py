""" Views """
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views import generic
from django.db.models import F
from django.utils import timezone

from .models import Question, Choice

class IndexView(generic.ListView):
    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions
        (not including those set to be published in the future)"""
        # return Question.objects.order_by('-pub_date')[:5]
        return Question.objects.filter(
                pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

class DetailView(generic.DetailView):
    model = Question
    template_name = 'polls/detail.html'
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(generic.DetailView):
    model = Question
    template_name = 'polls/results.html'

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        # Request.post: dictionary-like object that lets you access submitted data by a key name.
        # request.POST['choice'] returns the ID of the selected choice as a string.
        # request.POST always returns a string.
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the voting form
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
            })
    else:
        #selected_choice.votes += 1
        # Update directly in databse, to avoid race conflicts
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing with POST data
        # This prevents data from being posted twice if a user hits the back button.
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))




## Code that doesn't use generic views:
# def index(request):
#     latest_question_list = Question.objects.order_by('-pub_date')[:5]
#     context = {
#             'latest_question_list': latest_question_list,
#             }
#     #template = loader.get_template('polls/index.html')
#     #return HttpResponse(template.render(context, request))
#     ## Shortcut:
#     return render(request, 'polls/index.html',context)
#
# def detail(request, question_id):
#     # try:
#     #     question = Question.objects.get(pk=question_id)
#     # except Question.DoesNotExist:
#     #     raise Http404("Question does not exist")
#     ## Shortcut:
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/detail.html', context)
#
# def results(request, question_id):
#     question = get_object_or_404(Question, pk=question_id)
#     context = {'question': question}
#     return render(request, 'polls/results.html', context)


