from django import forms
from django.forms import ModelForm, Form
from main.models import Note, Text


class NoteForm(ModelForm):
    class Meta:
        model = Note
        fields = ('title',)
        labels = {
            'title': '英文帳の題名',
        }


class TextForm(ModelForm):
    class Meta:
        model = Text
        fields = ('sentence', 'translation')
        labels = {
            'sentence': 'English',
            'translation': '和訳文'
        }


