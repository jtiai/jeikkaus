'''
Jeikkaus main models

Created on Dec 26, 2009

@author: jtiai
'''
from django.db import models

from django.contrib.auth.models import User
from jeikkaus.utils import winner
from django.utils.translation import ugettext_lazy as _
import datetime
import pytz

class Match(models.Model):
    """
    Match setup
    """
    home_team = models.CharField(max_length=128)
    away_team = models.CharField(max_length=128)

    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    closing_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ('closing_time', )
        verbose_name = _('match')
        verbose_name_plural = _('matches')

    def __unicode__(self):
        return u'%s %s' % (self.title, self.score)

    @property
    def title(self):
        return u'%s - %s' % (self.home_team, self.away_team)

    @property
    def score(self):
        if self.home_score and self.away_score:
            return u'(%s - %s)' % (self.home_score, self.away_score)
        else:
            return u''

    @property
    def is_open(self):
        return datetime.datetime.now(pytz.utc) < self.closing_time

    def get_guess_for_user(self, user=None):
        if not hasattr(self, '_user_guess_cache'):
            try:
                self._user_guess_cache = Guess.objects.get(match=self, user=user)
            except Guess.DoesNotExist:
                self._user_guess_cache = None
        return self._user_guess_cache

class Guess(models.Model):
    """
    Guess of the game from the user
    """
    user = models.ForeignKey(User)
    match = models.ForeignKey(Match)

    home_score = models.IntegerField(null=True, blank=True)
    away_score = models.IntegerField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'match', )
        verbose_name = _('guess')
        verbose_name = _('guesses')

    def __unicode__(self):
        if self.home_score is None:
            home_score = u'x'
        else:
            home_score = self.home_score
        if self.away_score is None:
            away_score = u'x'
        else:
            away_score = self.away_score

        return u'%s - %s' % (home_score, away_score)

    def points(self):
        """
        Calculates points for guess:
          2 points if winner was right,
          1 point if home result was right,
          1 point if visitor result was right.
          Total of 4 points
        """

        pts = 0

        if self.match.is_open or self.home_score is None or self.away_score is None:
            return 0

        if self.home_score == self.match.home_score:
            pts += 1
        if self.away_score == self.match.away_score:
            pts += 1
        if winner(self) == winner(self.match):
            pts += 2

        return pts
