# Django crash course

Reproduction step-by-step of this course "[Python crash course](https://www.youtube.com/watch?v=e1IyzVyrLSU)"

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
