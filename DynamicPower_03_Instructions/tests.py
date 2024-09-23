from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot



class PlayerBot(Bot):

    def play_round(self):
       yield  P01_BeginPart2
       yield  P02_MatchWork, dict( testingHistory = ',3,5,8,2,7,7,10,-1,2,1,1,9,9,4' )
       yield  P03_RoundOverview
       yield  P04a_Stage1Details
       yield  P04b_Stage1Details,  dict(stage1Details = ',example,0,example,1,example,1')

       yield  P05a_Stage2Details
       yield  P05b_Stage2Details, dict(stage2Details = ',example,0,example,1,example,1')

       yield  P06_Calculator
       yield  P07_History
       yield  P08_AdditionalQuestions
       yield  P09_BeliefElicitation
       yield  P10_PersonalNormElicitation
       yield  P11_SocialNormElicitation