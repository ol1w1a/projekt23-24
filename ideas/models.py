from django.db import models
from django.db.models import Count
# Create your models here.

class Idea(models.Model):
    title = models.CharField(max_length=200, verbose_name="Tytuł pomysłu")
    description = models.TextField(verbose_name="Opis projektu")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    def get_vote_count(self):
        return self.votes.count()

class Vote(models.Model):
    idea = models.ForeignKey(Idea, on_delete=models.CASCADE, related_name='votes')
    session_id = models.CharField(max_length=200)

    class Meta:
        unique_together = ('idea', 'session_id')

