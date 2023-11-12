from django import forms 

from .models import Civilization, Entry

class CivilizationForm(forms.ModelForm):
    class Meta:
        model = Civilization
        fields = ['text']
        labels = {'text': ''}


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ['text']
        labels = {'text': ''}
        widgets = {'text': forms.Textarea(attrs={'cols': 80})}