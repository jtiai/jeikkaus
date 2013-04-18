# -*- encoding=utf-8 -*-
'''
Created on Jan 11, 2010

@author: jtiai
'''

from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('jeikkaus.views',
    url(r'^$', 'match_list', name='match_list'),
    url(r'^match/(?P<id>\d+)/$', 'match_details', name='match_details'),
    url(r'^guess/(?P<id>\d+)/$', 'guess', name='guessmatch'),
    url(r'^scoreboard/$', 'scoreboard', name='scoreboard'),
)
