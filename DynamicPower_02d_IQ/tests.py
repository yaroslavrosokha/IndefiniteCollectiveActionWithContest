from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):

    def play_round(self):
        if self.round_number == 1:
            yield page0
        yield  page1, dict(iqResponses = ',2')
