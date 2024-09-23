import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha / Xinxin Lyu'
doc = """
Demographic Questionnaire (Post-experiment Survey) 
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_07_Demographics'
    players_per_group = None
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    # Questionnaire
    ageSelect = models.StringField(
        choices=['Under 20', '20 and over', 'Prefer Not to Say'], verbose_name='Age:'
    )
    genderSelect = models.StringField(
        choices=['Male', 'Female', 'Prefer Not to Say'], verbose_name='Gender:'
    )
    majorSelect = models.StringField(
        choices=[
            'Economics or Management',
            'STEM (Science, Technology, Engineering, Math)',
            'Liberal Arts',
            'Other',
            'Prefer Not to Say',
        ],
        verbose_name='Major:',
    )
    hsSelect = models.StringField(
        choices=['In US', 'Outside of US', 'Prefer Not to Say'], verbose_name='Went to High School:'
    )


# FUNCTIONS
# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = ['ageSelect', 'genderSelect', 'majorSelect', 'hsSelect']


page_sequence = [
    Questionnaire,
]
