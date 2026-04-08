from django import apps
from django import forms
from .models import Idea

class IdeaForm(forms.ModelForm):
    class Meta:
        model = Idea
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Nazwa pomysłu '}),
            'description': forms.Textarea(attrs={'placeholder':'Opisz swój projekt '}),
        }