import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha / Xinxin Lyu'
doc = """
Post-experimental Questionnaire.
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_08_FeedbackQuestions'
    players_per_group = None
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    # Questionnaire
    understandingSelect = models.StringField(
        choices=['Clear', 'Somewhat Clear', 'Somewhat Confusing', 'Confusing'],
        verbose_name='Clarity of Instructions:',
        blank=True,
        widget=widgets.RadioSelectHorizontal,
    )
    explainedText = models.LongStringField(
        verbose_name='What could have been explained better?',
        blank=True,
    )
    strategy1Text = models.LongStringField(
        verbose_name='What was your strategy in part 2, stage 1? How did you choose the actions? (Please be specific)',
        blank=True,
    )
    strategy2Text = models.LongStringField(
        verbose_name='What was your strategy in part 2, stage 2? How did you decide the spend? (Please be specific)',
        blank=True,
    )
    strategy3Text = models.LongStringField(
        verbose_name='Do you think reporting your beliefs and the appropriateness of your actions influenced your decision? If so, in what way? (Please be specific)',
        blank=True,
    )
    strategy4Text = models.LongStringField(
        verbose_name='Did your decision in a round depend on what happened in the previous rounds? If so, in what way? (Please be specific)',
        blank=True,
    )
    strategy5Text = models.LongStringField(
        verbose_name='Was your strategy different between the initial matches and the later matches of the experiment? If so, in what way? (Please be specific)',
        blank=True,
    )


# FUNCTIONS
# PAGES
class Questionnaire(Page):
    form_model = 'player'
    form_fields = [
        'understandingSelect',
        'explainedText',
        'strategy1Text',
        'strategy2Text',
        'strategy3Text',
        'strategy4Text',
        'strategy5Text',
    ]

    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == Constants.num_rounds
    @staticmethod
    def vars_for_template(player: Player):
        return {'earningsTotal': player.participant.payoff_plus_participation_fee()}


page_sequence = [Questionnaire]
