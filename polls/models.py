"""
Poll Models
"""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib import admin

class Question(models.Model):
    """ Poll Question """
    question_text = models.CharField(max_length=200, default='Why?')
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    @admin.display(
            boolean=True,
            ordering='pub_date',
            description='Recent?'
            )
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

class Choice(models.Model):
    """ Poll Response Choice """
    # ForeignKey tells Django each Choice is related to a single Question.
    question = models.ForeignKey(Question,
            on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text
