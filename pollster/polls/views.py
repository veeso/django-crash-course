from django.http.response import Http404, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, parser_classes
from rest_framework.parsers import JSONParser

from .models import Question, Choice
from .serializers import QuestionSerializer, QuestionBriefSerializer

# Get questions and display then

def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] # Max 5 and sort by pub date
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context=context)

def detail(request, question_id: int):
    """
    Show speicific question and choices
    """
    # Get question or return 404 if failed
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/detail.html', context=context)

def results(request, question_id: int):
    """
    Show results for a question
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request, 'polls/results.html', context=context)

def vote(request, question_id: int):
    """
    Enregister the user vote
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choices.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select any choice"
        })
    else:
        # Increase choice counter and save
        selected_choice.votes += 1
        selected_choice.save()
        # Return results
        return HttpResponseRedirect(reverse('polls:results', args=(question_id,)))

@api_view(['GET'])
def questionList(request):
    questions = Question.objects.all().order_by('pub_date')
    serializer = QuestionBriefSerializer(questions, many=True) # Many indicates whether we want 1 or more elements
    return Response(serializer.data)

@api_view(['GET'])
def questionDetail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    serializer = QuestionSerializer(question, many=False) # Many indicates whether we want 1 or more elements
    return Response(serializer.data)

@api_view(['POST'])
@parser_classes([JSONParser])
def questionVote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    print(request.data)
    try:
        selected_choice = question.choices.get(pk=request.data['choice'])
    except KeyError:
        return HttpResponseBadRequest()
    except Choice.DoesNotExist:
        raise Http404
    else:
        # Increase choice counter and save
        selected_choice.votes += 1
        selected_choice.save()
    # Return updated question
    serializer = QuestionSerializer(question, many=False) # Many indicates whether we want 1 or more elements
    return Response(serializer.data)
