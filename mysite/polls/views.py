from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.http import Http404
from django.urls import reverse
from django.db.models import F
# Create your views here.

def index(request):
    lastest_question_list = Question.objects.order_by('-pub_date')[:5] #pub_date를 역순으로 정렬을 해서 다섯 개를 가지고 온다.
    context = {'questions': lastest_question_list}
    return render(request, 'polls/index.html', context)

def some_url(request):
    return HttpResponse("Some url을 구현해 봤습니다.")

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try: 
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {'question': question, 'error_message': '선택이 없습니다.'})
    else:
        selected_choice.votes = F('votes') + 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))

def result(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/result.html', {'question': question})