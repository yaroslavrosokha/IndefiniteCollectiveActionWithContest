from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
import time



class PlayerBot(Bot):

    def play_round(self):
        yield P00_BeginPart1
        yield p01_introduction, dict(practiceResponses='ABBBB',checkConfirm = 'True' )
        # time.sleep(5) 
        yield p02_compensationInstructions, dict(practiceTaskSelected = 1, practiceDecisionSelected = 3, practiceDrawSelected=30)
        # time.sleep(5) 
        yield p03_task, dict(responses = 'AAAAAAAAAAABBBBB', checkConfirm = 'True')
        # yield p03_task, dict(responses = 'AAAAAAAAAAABBBBB', checkConfirm = 'True')

        # time.sleep(5) 