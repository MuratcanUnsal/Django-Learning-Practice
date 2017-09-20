__author__ = 'Crashmotilda'
from django import forms
import django.utils.encoding


class PlayerSearchForm(forms.Form):

    query = forms.CharField(label= "Player" ,max_length=100, required=False)

    def __init__(self, query):
        super(PlayerSearchForm, self).__init__()
        self.fields['query'].initial = query


