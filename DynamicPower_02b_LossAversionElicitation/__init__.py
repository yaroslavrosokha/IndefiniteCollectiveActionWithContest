import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Loss Aversion Elicitation (ala Sheremeta)
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_02b_LossAversionElicitation'
    players_per_group = None
    num_rounds = 1
    safeOption2 = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
    safeOption2Practice = [0.5, 2.5, 5, 7.5, 10.0]
    riskySuccess = 8
    riskyFailure = 0


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    chosenPracticeQuestion = models.IntegerField()
    practiceResponses = models.StringField(initial="")
    checkConfirm = models.StringField()
    practiceTaskSelected = models.StringField()
    practiceDecisionSelected = models.StringField()
    practiceDrawSelected = models.StringField()
    responses = models.StringField()
    chosenQuestion = models.IntegerField()
    chosenTaskPart2 = models.IntegerField()
    chosenDraw = models.IntegerField()
    thisTaskEarn = models.IntegerField(initial=0)


# FUNCTIONS
# PAGES
def vars_for_admin_report(subsession):
    
    table_output = sorted([[p.id_in_subsession, p.thisTaskEarn ]  for p in subsession.get_players()])
    return dict(
                table_output = table_output,                
                )


class p03_task(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['responses', 'checkConfirm']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'offer_numbers': zip(range(1, len(Constants.safeOption2) + 1), Constants.safeOption2),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['LossAversionChoices'] = player.responses
        n = len(player.responses)
        player.chosenQuestion = int(np.random.choice(np.arange(n)) + 1)
        player.participant.vars['LossAversionQuestion'] = player.chosenQuestion
        player.chosenDraw = np.random.choice([-player.chosenQuestion * 0.5, 5.00], p=[0.5, 0.5])
        player.participant.vars['LossAversionDraw'] = player.chosenDraw
        if player.responses[player.chosenQuestion - 1] == 'A':
            player.participant.vars['LossAversionEarn'] = player.chosenDraw
        else:
            player.participant.vars['LossAversionEarn'] = 0.0
        player.thisTaskEarn = int(player.participant.vars['LossAversionEarn'])


page_sequence = [p03_task]
