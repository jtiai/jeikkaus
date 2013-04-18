# -*- encoding=utf-8 -*-
'''
Created on Jan 12, 2010

@author: jtiai
'''
from django import forms
from jeikkaus import models

class GuessModelForm(forms.ModelForm):
    class Meta:
        model = models.Guess
        exclude = ['user', 'match', ]
        