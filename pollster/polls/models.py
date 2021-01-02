from django.db import models

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
