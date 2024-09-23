from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):

    def play_round(self):
        yield p01_introduction
        yield page1, dict(myResponses1 = ',2,2,2,2,2,2,2,2,2,2')
        
        yield page2, dict(myResponses2 = ',2,2,2,2,2,2,2,2,2,2')
        yield page3, dict(myResponses3 = ',2,2,2,2,2,2,2,2,2,2')
        yield page4, dict(myResponses4 = ',2,2,2,2,2,2,2,2,2,2')
        yield page5, dict(myResponses5 = ',2,2,2,2,2,2,2,2,2,2')
        yield page6, dict(myResponses6 = ',2,2,2,2,2,2,2,2,2,2')
        yield page7, dict(myResponses7 = ',2,2,2,2,2,2')
