from otree.api import Currency as c, currency_range

from . import *
from otree.api import Bot



class PlayerBot(Bot):

    def play_round(self):
            
            
        yield beginQuiz
        yield Question1_2, dict(quizHistory1='something', quiz1_D=0,quiz1_1C=0)
        yield Question3, dict(quizHistory2='something', quiz2=0)
        # yield Question4, dict(quizHistory3='something', quiz3=0)
        # yield Question5_7, dict(quizHistory4='something',  quiz5=0, quiz6=0)
        yield Question8, dict(quizHistory7='something')
        yield Question9, dict(quizHistory8='something')
        yield Question10, dict(quizHistory9= 'something')
        yield Question11, dict(quizHistory10 ='something')
