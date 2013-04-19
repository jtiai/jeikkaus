'''
Created on Jan 10, 2010

@author: jtiai
'''
from django.contrib import admin
from jeikkaus import models

class MatchAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'home_score', 'away_score', 'closing_time', 'is_open' )
    list_display_links = ('__unicode__', )
    list_editable = ('home_score', 'away_score',  )
    
admin.site.register(models.Match, MatchAdmin)

admin.site.register(models.Guess)
