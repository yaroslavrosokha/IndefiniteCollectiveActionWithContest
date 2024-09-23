import numpy as np
from otree.api import *


author = 'Xinxin Lyu '
doc = """
    Based on Sunk Cost Elicitation by Yaroslav Rosokha
    Social preference elicitation (Kerschbamer, 2015)
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_02c_SocialPreference'
    players_per_group = None
    num_rounds = 1
    safeOption2 = [
        3.0,
        3.25,
        3.5,
        3.75,
        4.0,
        4.25,
        4.5,
        4.75,
        5.0,
    ]
    other1 = 2.5
    other2 = 5.5
    equalPay = 4.0




class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    chosenPracticeQuestion = models.IntegerField()
    practiceResponses = models.StringField()
    checkConfirm = models.StringField()
    practiceTaskSelected = models.StringField()
    practiceDecisionSelected = models.StringField()
    practiceDrawSelected = models.StringField()
    responses0 = models.StringField()
    responses1 = models.StringField()
    responses2 = models.StringField()
    
    moneyReceived = models.FloatField()

    chosenQuestion = models.IntegerField()
    chosenTaskPart2 = models.IntegerField()
    chosenDraw = models.IntegerField()
    
    thisTaskEarn = models.IntegerField(initial=0)
    thisTaskSend = models.IntegerField(initial=0)

# FUNCTIONS
def vars_for_admin_report(subsession):
    
    table_output = sorted([[p.id_in_subsession, p.thisTaskEarn, p.thisTaskSend ]  for p in subsession.get_players()])
    return dict(
                table_output = table_output,                
                )
                
def set_receivedMoney(group):
    for p in group.get_players():
        if p.id_in_group == p.session.num_participants :
            id_sendMoneyto = 1
        else :
            id_sendMoneyto = p.id_in_group + 1
            
        for r in group.get_players(): 
            if r.id_in_group == id_sendMoneyto:
                r.moneyReceived = p.participant.vars['SocialPreferenceEarn_other']
                r.participant.vars['MoneyReceived'] = p.participant.vars['SocialPreferenceEarn_other']
            
        
               
        
# PAGES
class p01_introduction(Page):
    """Description of the game: How to play and returns expected"""
    form_model = 'player'
    form_fields = ['responses0']

    @staticmethod
    def vars_for_template(player: Player):
        safeOption2Practice = [3,4,5]
        return {
            'offer_numbers': zip(range(1, len(safeOption2Practice) + 1), safeOption2Practice),
        }


class p03_task(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['responses1', 'checkConfirm']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'offer_numbers1': zip(range(1, len(Constants.safeOption2) + 1), Constants.safeOption2),
        }



class p04_task(Page):
    """Description of the game: How to play and returns expected"""

    form_model = 'player'
    form_fields = ['responses2', 'checkConfirm']

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'offer_numbers2': zip(range(1, len(Constants.safeOption2) + 1), Constants.safeOption2),
        }

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['SocialPreferenceChoices'] = player.responses1 + player.responses2
        responses = player.responses1 + player.responses2
        n = len(responses)
        player.chosenQuestion = int(np.random.choice(np.arange(n)) + 1)
        player.participant.vars['SocialPreferenceQuestion'] = player.chosenQuestion
        if responses[player.chosenQuestion - 1] == 'B':
            
            if player.chosenQuestion - 1 <=  8 :
                player.participant.vars['SocialPreferenceEarn_me'] = Constants.safeOption2[player.chosenQuestion - 1]
                player.participant.vars['SocialPreferenceEarn_other'] =     Constants.other1
            else :
                player.participant.vars['SocialPreferenceEarn_me'] = Constants.safeOption2[player.chosenQuestion - 10]
                player.participant.vars['SocialPreferenceEarn_other'] =  Constants.other2
        else:
            player.participant.vars['SocialPreferenceEarn_me'] = Constants.equalPay
            player.participant.vars['SocialPreferenceEarn_other'] = Constants.equalPay

        player.thisTaskEarn = int(player.participant.vars['SocialPreferenceEarn_me'])
        player.thisTaskSend = int(player.participant.vars['SocialPreferenceEarn_other'])

        
        
class WaitForOthers(WaitPage):
    template_name = 'DynamicPower_02c_SocialPreference/myWaitPage.html'
    after_all_players_arrive = set_receivedMoney
    @staticmethod
    def vars_for_template(player: Player):
        title_text = ""
        body_text = "Please wait for other participants to finish Tasks 1--4."
        return {'title_text': title_text, "body_text": body_text}


page_sequence = [p01_introduction, p03_task, p04_task, WaitForOthers]
