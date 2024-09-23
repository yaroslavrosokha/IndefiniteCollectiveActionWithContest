from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Introduction to Dynamic Power Repeated Games Experiment
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_02_Introduction'
    min_payment = 5
    players_per_group = None
    duration = 90
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    pass


# FUNCTIONS
# PAGES



class P01_Overview(Page):
    pass


page_sequence = [
    P01_Overview,
]
