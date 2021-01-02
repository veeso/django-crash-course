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
    >>> q.choice_set.create(choice_text = "C/C++")
    >>> q.choice_set.create(choice_text = "JavaScript")
    >>> q.choice_set.create(choice_text = "Rust")
    >>> q.choice_set.create(choice_text = "Python")
    >>> q.choice_set.create(choice_text = "Java")
    >>> q.choice_set.create(choice_text = "CSharp")
    >>> q.choice_set.create(choice_text = "Go")
    >>> q.choice_set.create(choice_text = "PHP")
    >>> q.choice_set.create(choice_text = "Ruby")
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
