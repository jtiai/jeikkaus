'''
Created on Jan 5, 2010

@author: jtiai
'''

HOME = 1
VISITOR = -1
TIE = 0

def winner(self):
    """Returns winner of the match or guess
    1 = home, 0 = equal, -1 = visitor"""
    if self.home_score > self.away_score:
        return HOME
    elif self.home_score < self.away_score:
        return VISITOR
    else:
        return TIE