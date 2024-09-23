from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import time


class PlayerBot(Bot):

    def play_round(self):
        yield (PaymentInfo)
        time.sleep(10) 