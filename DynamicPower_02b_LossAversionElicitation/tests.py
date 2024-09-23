from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot

import time


class PlayerBot(Bot):

    def play_round(self):
        yield p03_task, dict(responses = 'AAAAAAAAAAABBBBB', checkConfirm = 'True')
        # time.sleep(5) 