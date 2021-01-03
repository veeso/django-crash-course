# Django crash course

Reproduction step-by-step of this course "[Python crash course](https://www.youtube.com/watch?v=e1IyzVyrLSU)"

---

- [Django crash course](#django-crash-course)
  - [Steps](#steps)
    - [Setup](#setup)
    - [Define the model](#define-the-model)
    - [Add records](#add-records)
    - [Enter admin area](#enter-admin-area)
    - [Add to administration a form to add polls](#add-to-administration-a-form-to-add-polls)
    - [Create the first view](#create-the-first-view)
    - [Make HTML templates](#make-html-templates)
    - [Show questions in index](#show-questions-in-index)
  - [Tutorial expansion](#tutorial-expansion)
    - [Create a REST API](#create-a-rest-api)

---

## Steps

### Setup

1. Install pipenv

    `sudo -H pip3 install pipenv`

2. Create pipenv dependencies file

    `pipenv shell`

3. Install django in environment

    `pipenv install django`

4. Create django pollster project

    `django-admin startproject pollster`

    These files are created

      - pollster/
        - asgi.py
        - settings.py: contains django configuration (production secret key, database, tzconfig...)
        - urls.py: contains url managed by the application
        - wsgi.py

5. Run installed django environment (for testing)

    `cd pollster/ && python3 manage.py runserver`

6. Run migrations (to create default database)

    `python3 manage.py migrate`

7. Create app (polls)

    `python3 startapp polls`

8. Add polls to apps

    move to `pollster/pollster/settings.py`
    and add to `INSTALLED_APPS` the entry `'polls.apps.PollsConfig'`

### Define the model

We're then going to define the model for our poll applications. These entities will then be created into the database, when running the migration.

1. move to `pollster/polls/models.py`
2. Define models

    ```py
    class Question(models.Model):
        """
        Question represents a poll
        """
        question_text = models.CharField(max_length=256)
        pub_date = models.DateTimeField("publication date")

        def __str__(self) -> str:
            return self.question_text

    class Choice(models.Model):
        """
        Choice represents a choice for a certain ``Question``
        """
        # If a question is deleted, all related choices are deleted -> `on_delete = models.CASCADE`
        question = models.ForeignKey(Question, on_delete=models.CASCADE)
        choice_text = models.CharField(max_length=256)
        votes = models.IntegerField(default=0)

        def __str__(self) -> str:
            return self.choice_text
    ```

3. Make migrations

    run `python manage.py makemigrations polls`

4. Run migrations

    as before `python3 manage.py migrate`

### Add records

1. Run shell and add a new Question entity

    ```sh
    python manage.py shell
    >>> from django.utils import timezone
    >>> from polls.models import Question, Choice
    >>> q = Question(question_text = "What is your favourite Programming language?", pub_date=timezone.now())
    >>> q.save()
    >>> q.id
    >>> q.question_text
    >>> Questions.objects.all()
    ```

2. Add a new Choice

    ```sh
    python manage.py shell
    >>> q = Question.objects.get(pk = 1)
    >>> q.choices.create(choice_text = "C/C++")
    >>> q.choices.create(choice_text = "JavaScript")
    >>> q.choices.create(choice_text = "Rust")
    >>> q.choices.create(choice_text = "Python")
    >>> q.choices.create(choice_text = "Java")
    >>> q.choices.create(choice_text = "CSharp")
    >>> q.choices.create(choice_text = "Go")
    >>> q.choices.create(choice_text = "PHP")
    >>> q.choices.create(choice_text = "Ruby")
    >>> q.save()
    >>> quit()
    ```

### Enter admin area

1. Create super user

    ```sh
    python manage.py createsuperuser
    Username (leave blank to use '${USER}'): 
    Email address: christian.visintin@*********
    Password:
    Password (again):
    This password is too short. It must contain at least 8 characters.
    Bypass password validation and create user anyway? [y/N]: y
    Superuser created successfully.
    ```

2. Run server

    `python manage.py runserver`

3. Go to admin page

    from your browser: `http://localhost:8000/admin`

4. Access with your credentials

### Add to administration a form to add polls

1. Move to `pollster/polls/admin.py`
2. Let's add models

    ```py
    from .models import Question, Choice

    admin.site.register(Question)
    admin.site.register(Choice)
    ```
  
    Now you're finally able to add Questions and choices to the database.

3. Let's make it cooler

    ```py
    # Register your models here.
    from .models import Question, Choice

    class ChoiceInline(admin.TabularInline):
        model = Choice
        extra = 3 # Default choices entries

    class QuestionAdmin(admin.ModelAdmin):
        fieldsets = [
            (None, {'fields': ['question_text']}),
            ('Date Information', {'fields': ['pub_date'], 'classes': ['collapse']}),
        ]
        inlines = [ChoiceInline]

    #admin.site.register(Question)
    #admin.site.register(Choice)
    admin.site.register(Question, QuestionAdmin)
    ```

4. (Extra) add header and title for administration

    ```py
    # Set website header
    admin.site.site_header = "Pollster Admin"
    admin.site.site_title = "Pollster Admin Area"
    admin.site.index_title = "Welcome to Pollster administration"
    ```

### Create the first view

1. Move to `pollster/polls/views.py`
2. Show questions
3. Add index definition

    ```py
    from .models import Question, Choice

    # Get questions and display then

    def index(request):
        return render(request, 'polls/index.html')
    ```

4. Define url

    Create `pollster/polls/urls.py`
    and type

    ```py
    from django.urls import path

    # Import views
    from . import views

    # Give app a name
    app_name = "polls"
    urlpatterns = [
        path('', views.index, name='index') # /polls/index.html
    ]
    ```

5. Add polls url to pollster urls

    Move to `pollster/pollster/urls.py`

    and add change `urlpatterns` to:

    ```py
    # Add include
    from django.urls import path, include
    # ...
    # Add here
    urlpatterns = [
      path('admin/', admin.site.urls),
      path('polls/', include('polls.urls')),
    ]
    ```

6. Add templates folder in `pollster/templates`
7. Add index.html to `pollster/templates/polls/index.html`
8. Set templates as global folder

    move to `pollster/pollster/settings.py`
    and to `TEMPLATES`
    add `'DIRS': [os.path.join(BASE_DIR, 'templates')],`

### Make HTML templates

1. Let's make base html template at `pollster/templates/base.html`
2. Extend base in `pollster/templates/polls/index.html`

    ```html
    {% extends 'base.html' %}
    {% block content %}
      POLLS
    {% endblock %}
    ```

### Show questions in index

1. Move to `pollster/polls/views.py`

    ```py
    def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5] # Max 5 and sort by pub date
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context=context)
    ```

2. Add implementation for `index.html`

    ```html
    {% extends 'base.html' %}
    {% block content %}
      <h1 class="text-center mb-3">Poll questions</h1>
      {% if latest_question_list %}
        {% for question in latest_question_list %}
          <div class="card mb-3">
            <div class="card-body">
              <h2 class="lead">
                {{ question.question_text }}
              </h2>
              <a href="{% url 'polls:detail' question.id %}" class="btn btn-primary btn-sm">Vote now!</a>
              <a href="{% url 'polls:results' question.id %}" class="btn btn-secondary btn-sm">View results</a>
            </div>
          </div>
        {% endfor %}
      {% else %}
        <h2 class="text-center mb-3">No polls available</h2>
      {% endif %}
    {% endblock %}
    ```

3. Let's implement details

    Move to `pollster/polls/views.py`

    ```py
    def detail(request, question_id):
        """
        Show speicific question and choices
        """
        try:
            # Get question by id
            question = Question.objects.get(pk=question_id)
        except Question.DoesNotExist:
            # Return 404
            raise Http404
        context = {'question': question}
        return render(request, 'polls/detail.html', context=context)
    ```

4. Let's implement results

    ```py
    def results(request, question_id: int):
        """
        Show results for a question
        """
        question = get_object_or_404(Question, pk=question_id)
        context = {'question': question}
        return render(request, 'polls/results.html', context=context)
    ```

5. Add other pages to `pollster/polls/urls.py`

    ```py
    urlpatterns = [
        path('', views.index, name='index'), # /polls/index.html
        path('<int:question_id>', view=views.detail, name='detail'),
        path('<int:question_id>', view=views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
    ]
    ```

6. Add results.html and detail.html
7. Add vote

    ```py
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
    ```

---

## Tutorial expansion

This part is not included in the django crash course video, but I included since I found it useful.

### Create a REST API

Let's create a REST API to interact with the poll application.
We'll implement the following methods

- GET /polls/api/questions

which will return an object with all questions summary

```json
[
    {
        "id": 1,
        "text": "What's your favourite programming language?"
    }
]
```

- GET /polls/api/question/{ID}

which will return an object with the question details and choices

```json
[
    {
        "id": 1,
        "text": "What's your favourite programming language?",
        "choices": [
            {
                "id": 1,
                "text": "Rust",
                "votes": 2
            },
            {
                "id": 2,
                "text": "C/C++",
                "votes": 1
            }
        ]
    }
]
```

- POST /polls/api/vote/{QUESTION_ID}

which will enregister the vote for a certain poll

```json
{
    "choice": 2
}
```

Let's see the implementation step-by-step.

Setup:

1. Install Django REST Framework

    ```sh
    pip install djangorestframework
    ```

2. Tell Django we've installed the REST framework

    Move to `pollster/pollster/settings.py`

    ```py
    INSTALLED_APPS = [
    #...
    'rest_framework',
    ]
    ```

Let's create the GET request

1. Add `related_name` to `Choice` in models:

    Move to `pollster/polls/models.py`

    ```py
    class Choice(models.Model):
        """
        Choice represents a choice for a certain ``Question``
        """
        # If a question is deleted, all related choices are deleted -> `on_delete = models.CASCADE`
        question = models.ForeignKey(Question, related_name='choices', on_delete=models.CASCADE)
        #...
    ```

2. Create serializers

    move to `pollster/polls/serializers.py`

    ```py
    # Import serializers from REST framework
    from rest_framework import serializers
    # Import our models
    from .models import Question, Choice

    class QuestionBriefSerializer(serializers.HyperlinkedModelSerializer):
        class Meta:
            model = Question
            fields = ('question_text', 'pub_date')

    class QuestionSerializer(serializers.HyperlinkedModelSerializer):
        # Add choices to relations and serialize it using the `ChoiceSerializer`
        choices = ChoiceSerializer(many=True)
        class Meta:
            model = Question
            fields = ('question_text', 'pub_date', 'choices')

    ```

3. Display data in views

    move to `pollster/polls/views.py`

    ```py
    from rest_framework.response import Response
    from rest_framework.decorators import api_view
    from .serializers import QuestionSerializer, QuestionBriefSerializer
    #...
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
    
    ```

4. Add URLs and router

    Move to `pollster/polls/urls.py`

    ```py
    from django.urls import path

    # Import views
    from . import views
    
    # Give app a name
    app_name = "polls"
    urlpatterns = [
        path('', views.index, name='index'), # /polls/index.html
        path('<int:question_id>/', views.detail, name='detail'),
        path('<int:question_id>/results', views.results, name='results'),
        path('<int:question_id>/vote/', views.vote, name='vote'),
        path('api/questions/', views.questionList, name='questions'),
        path('api/question/<int:question_id>/', views.questionDetail, name="question"),
    ]
    ```

Now you should finally be able to perform a GET to `http://localhost:8000/polls/api/questions`

Let's implement the vote POST method.

1. Add request to view

    ```py
    @api_view(['POST'])
    @parser_classes([JSONParser])
    def questionVote(request, question_id):
        question = get_object_or_404(Question, pk=question_id)
        print(request.data)
        try:
            selected_choice = question.choices.get(pk=request.data['choice'])
        except (KeyError, Choice.DoesNotExist):
            raise Http404
        else:
            # Increase choice counter and save
            selected_choice.votes += 1
            selected_choice.save()
        # Return updated question
        serializer = QuestionSerializer(question, many=False) # Many indicates whether we want 1 or more elements
        return Response(serializer.data)
    ```

2. Add URL

    ```py
    path('api/vote/<int:question_id>', views.questionVote, name="vote"),
    ```

And that's all.