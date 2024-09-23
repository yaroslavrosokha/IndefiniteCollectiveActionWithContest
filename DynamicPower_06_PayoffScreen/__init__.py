from otree.api import *
import numpy as np


author = 'Yaroslav Rosokha / Xinxin Lyu'
doc = """
Payoff information.
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_06_PayoffScreen'
    players_per_group = None
    num_rounds = 1
    
    # Risk aversion  / # Loss aversion 
    safeOption2 = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8]
    riskySuccess = 8
    riskyFailure = 0

    # For Social Preference
    safeOption =  [
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
    flatPay = 4.0

class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    Chosen_Task =  models.IntegerField()
    MatchesPayoff = models.CurrencyField(initial = 0)
    ReceivMoneyDummy = models.IntegerField(initial = 0)
    ReceivedMoney = models.CurrencyField(initial = 0)

# FUNCTIONS
def creating_session(subsession):
    import random
    for player in subsession.get_players():
        
        # player.Chosen_Task =  int(np.random.choice(np.arange(6)) + 1)
        player.Chosen_Task =  int(np.random.choice(np.arange(5)) + 1)
        if player.Chosen_Task  == 3 or player.Chosen_Task  == 4 :
            if player.id_in_group == player.session.num_participants :
                id_sendMoneyto = 1
            else :
                id_sendMoneyto = player.id_in_group + 1
            for r in subsession.get_players():        
                if r.id_in_group == id_sendMoneyto :
                    r.ReceivMoneyDummy = 1



# PAGES

class FinalPaymentWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group: Group):
        for player in group.get_players():
            player.MatchesPayoff = player.participant.payoff
            if player.ReceivMoneyDummy == 1 :
                player.ReceivedMoney = player.participant.vars['MoneyReceived']
                player.participant.payoff += player.ReceivedMoney  / player.session.config['real_world_currency_per_point']
            
                        
            if player.Chosen_Task == 1 :
               player.participant.payoff += player.participant.vars['RiskAversionEarn'] / player.session.config['real_world_currency_per_point']
            elif player.Chosen_Task == 2 :
               player.participant.payoff += player.participant.vars['LossAversionEarn'] / player.session.config['real_world_currency_per_point']
            elif player.Chosen_Task == 3 or   player.Chosen_Task == 4: 
                player.participant.payoff += player.participant.vars['SocialPreferenceEarn_me'] / player.session.config['real_world_currency_per_point']
            else :
                player.participant.payoff += Constants.flatPay / player.session.config['real_world_currency_per_point']
                
            if player.participant.payoff < 0:
                player.participant.payoff  = 0
    
### Change EarnBelief5 to EarnBelief25 below ###
class PaymentInfo(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.participant.vars['totalPayoffs'] = player.participant.payoff.to_real_world_currency(
            player.session
        )

    @staticmethod
    def is_displayed(player):

        return   player.round_number == Constants.num_rounds
    
    @staticmethod
    def vars_for_template(player: Player):
        
        if player.participant.vars['SocialPreferenceQuestion']-1 <= 8 :
            others =  Constants.other1
            me = Constants.safeOption[player.participant.vars['SocialPreferenceQuestion']-1]
        else :    
            others =  Constants.other1
            me = Constants.safeOption[player.participant.vars['SocialPreferenceQuestion']-10]

        
        return {
            'MatchesPayoff': player.MatchesPayoff ,
            'TotalPayoff': player.participant.payoff_plus_participation_fee(),
            'Matches': player.session.config['Matches'],
            
            'Chosen_Task' : player.Chosen_Task, 
            'RiskAversionEarn' : player.participant.vars['RiskAversionEarn'],
            'RiskAversionChoices' : player.participant.vars['RiskAversionChoices'][ player.participant.vars['RiskAversionQuestion']-1],
            'RiskAversionQuestion' : player.participant.vars['RiskAversionQuestion'],
            'RiskAversionQuestion_optionA' : Constants.safeOption2[player.participant.vars['RiskAversionQuestion']-1],
            
            'LossAversionEarn' : player.participant.vars['LossAversionEarn'],
            'LossAversionChoices' : player.participant.vars['LossAversionChoices'][ player.participant.vars['LossAversionQuestion']-1],
            'LossAversionQuestion' : player.participant.vars['LossAversionQuestion'],
            'LossAversionQuestion_optionA' : Constants.safeOption2[player.participant.vars['LossAversionQuestion']-1],

            'SocialPreferenceChoices' : player.participant.vars['SocialPreferenceChoices'][ player.participant.vars['SocialPreferenceQuestion']-1],
            'SocialPreferenceQuestion' : player.participant.vars['SocialPreferenceQuestion'],
            'SocialPreferenceEarn_me' : player.participant.vars['SocialPreferenceEarn_me'],
            'SocialPreferenceEarn_other' : player.participant.vars['SocialPreferenceEarn_other'],
            'SocialPreferenceQuestion_optionA' : me, 
            'SocialPreferenceQuestion_optionAothers' : others ,
            'MoneyReceived' : player.ReceivedMoney,
            
            'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),

            
            
        
        }

    


page_sequence = [FinalPaymentWaitPage, PaymentInfo]
