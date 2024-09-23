import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Risk Aversion Elicitation (ala Holt-Laury)
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_01a_RiskAversionElicitation'
    players_per_group = None
    num_rounds = 1
    safeOption2 = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
    safeOption2Practice = [ 0.5, 2, 4, 6, 8 ]
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


class P00_BeginPart1(Page):
    pass
    
class p01_introduction(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['practiceResponses', 'checkConfirm']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'offer_numbers': zip(
                range(1, len(Constants.safeOption2Practice) + 1), Constants.safeOption2Practice
            )
        }

    @staticmethod
    def is_displayed(player: Player):
        player.chosenPracticeQuestion = int(np.random.choice(np.arange(5)) + 1)
        player.chosenQuestion = int(np.random.choice(np.arange(5)) + 1)
        return player.subsession.round_number == 1


class p02_compensationInstructions(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['practiceTaskSelected', 'practiceDecisionSelected', 'practiceDrawSelected']

    @staticmethod
    def vars_for_template(player: Player):
        temp = {
            'offer_numbers': zip(
                range(1, len(Constants.safeOption2Practice) + 1), Constants.safeOption2Practice
            )
        }
        temp['practiceResponses'] = player.practiceResponses
        temp['chosenPracticeQuestion'] = player.chosenPracticeQuestion
        return temp

    @staticmethod
    def js_vars(player):
        return dict(
            safeOptions = Constants.safeOption2,
            safeOptions1 = Constants.safeOption2Practice,
            riskySuccess = Constants.riskySuccess,
            riskyFailure = Constants.riskyFailure,
            practiceResponses = player.practiceResponses, 
            )
    
    
    
class p03_task(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['responses', 'checkConfirm']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'offer_numbers': zip(range(1, len(Constants.safeOption2) + 1), Constants.safeOption2)
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['RiskAversionChoices'] = player.responses
        n = len(player.responses)
        player.chosenQuestion = int(np.random.choice(np.arange(n)) + 1)
        player.participant.vars['RiskAversionQuestion'] = player.chosenQuestion
        player.chosenDraw = int(np.random.choice([10, 0], p=[0.5, 0.5]))
        player.participant.vars['RiskAversionDraw'] = player.chosenDraw
        if player.responses[player.chosenQuestion - 1] == 'A':
            player.participant.vars['RiskAversionEarn'] = player.chosenDraw
        else:
            player.participant.vars['RiskAversionEarn'] = player.chosenQuestion * 0.5

        player.thisTaskEarn = int(player.participant.vars['RiskAversionEarn'])

class WaitForOthers(WaitPage):
    template_name = 'DynamicPower_01c_SocialPreferenceElicitation/myWaitPage.html'

    @staticmethod
    def vars_for_template(player: Player):
        print("RiskAversion,WaitForOthers()...")
        title_text = "Please wait for other participants..."
        body_text = ""
        return {'title_text': title_text, "body_text": body_text}


page_sequence = [P00_BeginPart1, p01_introduction, p02_compensationInstructions, p03_task]
