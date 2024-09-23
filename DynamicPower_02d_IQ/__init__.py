import random
import time

import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
ICAR 11-item Matrix Reasoning Test 
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_02d_IQ'
    players_per_group = None
    num_rounds = 11
    figNames = [
        'fig12043.jpg',
        'fig12044.jpg',
        'fig12045.jpg',
        'fig12046.jpg',
        'fig12047.jpg',
        'fig12048.jpg',
        'fig12050.jpg',
        'fig12053.jpg',
        'fig12054.jpg',
        'fig12055.jpg',
        'fig12056.jpg',
    ]


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass

   

class Player(BasePlayer):
    iqResponses = models.StringField()
    myOrder = models.StringField()


# FUNCTIONS
def creating_session(subsession):
    if subsession.round_number == 1:
        for p in subsession.get_players():
            print("here reached?")
            order = list(range(1, 11 + 1))
            # random.shuffle(order) #randomize order of questions
            p.participant.vars['iqOrder'] = dict(zip(range(1, 11 + 1), order))
            out = ""
            for x in order:
                out += "," + str(x)
            p.myOrder = out
 


# PAGES
class page0(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # user has 7 minutes to complete as many pages as possible
        
        player.participant.vars['expiryIQ'] = time.time() + 7 * 60

    @staticmethod
    def is_displayed(player: Player):
        
        return player.subsession.round_number == 1
        
    
class page1(Page):
    timer_text = 'Time Left:'

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryIQ'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        
        return player.participant.vars['expiryIQ'] - time.time() > 1

    form_model = 'player'
    form_fields = ['iqResponses']

    @staticmethod
    def vars_for_template(player: Player):
        
        return {
            'image_path': 'StrategyChoiceIQ/{}'.format(Constants.figNames[player.participant.vars['iqOrder'][player.round_number] - 1])
        }


page_sequence = [
    page0,
    page1,
]
