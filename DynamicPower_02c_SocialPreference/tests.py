from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import time


class PlayerBot(Bot):

    def play_round(self):
            yield p01_introduction
            # time.sleep(5) 
            yield p03_task, dict(responses1 = 'BBBBBBAAA', checkConfirm = 'True')
            # time.sleep(5)
            yield p04_task, dict( responses2 = 'BBBBAAAAA', checkConfirm = 'True')