from django.db import models
from django.contrib.auth.models import User
from django_mysql.models import ListCharField


class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    title = models.CharField('題名', max_length=20)
    # desc = models.CharField('詳細', max_length=50, blank=True)
    # public = models.BooleanField('公開/非公開', default=False)


class Text(models.Model):
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    sentence = models.CharField(max_length=800, default="")
    words = ListCharField(models.CharField(max_length=20), size=40, max_length=(21 * 40), default="")
    if_hide = ListCharField(models.CharField(max_length=1), size=40, max_length=(2 * 40), default="")
    translation = models.CharField(max_length=400)


class Fav(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)


class NoteLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    note = models.ForeignKey(Note, on_delete=models.CASCADE)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
