import random
import time

import numpy as np
from otree.api import *


author = 'Xinxin Lyu & Yaroslav Rosokha'
doc = """
Personality Questionnaire. 
66-items: 
    6 Machiavellianism (JPI: Social Astuteness [Sas]) ;
    10 C6: CAUTIOUSNESS (.76)
    10 Trust (NEO: A1);
    6 Competitiveness (HPI: Competitive HIC);
    10 C4: ACHIEVEMENT-STRIVING (.78);
    10 A4: COOPERATION (.73);
    10 Equity/Fairness (HEX: H-Fair);
    10 A3: ALTRUISM (.77);
    
    
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_02e_Personality'
    players_per_group = None
    num_rounds = 1
    numQuestions = 66
    questions = [
                "I find it easy to manipulate others.",
                "I have a natural talent for influencing people.",
                "I can talk others into doing things.",
                "I find it difficult to manipulate others.",
                "I hate being the center of attention.",
                "I lack the talent for influencing people.",
                "I avoid mistakes.",
                "I choose my words with care.",
                "I stick to my chosen path.",
                "I jump into things without thinking.",
                "I make rash decisions.",
                "I like to act on a whim.",
                "I rush into things.",
                "I do crazy things.",
                "I act without thinking.",
                "I often make last-minute plans.",
                "I trust others.",
                "I believe that others have good intentions.",
                "I trust what people say.",
                "I believe that people are basically moral.",
                "I believe in human goodness.",
                "I think that all will be well.",
                "I distrust people.",
                "I suspect hidden motives in others.",
                "I am wary of others.",
                "I believe that people are essentially evil.",
                "I go straight for the goal.",
                "I work hard.",
                "I turn plans into actions.",
                "I plunge into tasks with all my heart.",
                "I do more than what's expected of me.",
                "I set high standards for myself and others.",
                "I demand quality.",
                "I am not highly motivated to succeed.",
                "I do just enough work to get by.",
                "I put little time and effort into my work.",
                "I am easy to satisfy.",
                "I can't stand confrontations.",
                "I hate to seem pushy.",
                "I have a sharp tongue.",
                "I contradict others.",
                "I love a good fight.",
                "I yell at people.",
                "I insult people.",
                "I get back at others.",
                "I hold a grudge.",
                "I would never take things that aren't mine.",
                "I would never cheat on my taxes.",
                "I return extra change when a cashier makes a mistake.",
                "I would feel very badly for a long time if I were to steal from someone.",
                "I try to follow the rules.",
                "I admire a really clever scam.",
                "I cheat to get ahead.",
                "I steal things.",
                "I cheat on people who have trusted me.",
                "I would not regret my behavior if I were to take advantage of someone impulsively.",
                "I make people feel welcome.",
                "I anticipate the needs of others.",
                "I love to help others.",
                "I am concerned about others.",
                "I have a good word for everyone.",
                "I look down on others.",
                "I am indifferent to the feelings of others.",
                "I make people feel uncomfortable.",
                "I turn my back on others.",
                "I take no time for others."
    ]


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass

class Player(BasePlayer):
    myResponses1 = models.StringField()
    myResponses2 = models.StringField()
    myResponses3 = models.StringField()
    myResponses4 = models.StringField()
    myResponses5 = models.StringField()
    myResponses6 = models.StringField()
    myResponses7 = models.StringField()
    myOrder = models.StringField()


# FUNCTIONS
def creating_session(self):
    if self.round_number == 1:
        for p in self.get_players():
            randomOrder = [48,
                             12,
                             21,
                             3,
                             56,
                             22,
                             16,
                             40,
                             41,
                             18,
                             32,
                             35,
                             44,
                             10,
                             5,
                             36,
                             45,
                             53,
                             57,
                             52,
                             11,
                             39,
                             27,
                             60,
                             19,
                             23,
                             17,
                             66,
                             63,
                             34,
                             49,
                             51,
                             28,
                             50,
                             2,
                             1,
                             14,
                             65,
                             62,
                             54,
                             43,
                             13,
                             4,
                             15,
                             30,
                             24,
                             26,
                             37,
                             31,
                             46,
                             6,
                             55,
                             33,
                             58,
                             59,
                             9,
                             42,
                             29,
                             47,
                             38,
                             7,
                             8,
                             25,
                             20,
                             61,
                             64]
            # randomOrder = list(range(1,66+1))
            # random.shuffle(randomOrder)
            p.participant.vars['bigFiveOrder'] = dict(zip(range(1, 66 + 1), randomOrder))
            out = ""
            for x in randomOrder:
                out += "," + str(x)
            p.myOrder = out


# PAGES
class p01_introduction(Page):
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        # user has 6 minutes to complete as many pages as possible
        player.participant.vars['expiryPersonality'] = time.time() + 6 * 60


class page1(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses1']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(1, 10 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(1, 10 + 1), tempQ1)}


class page2(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses2']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(11, 20 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(11, 20 + 1), tempQ1)}


class page3(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses3']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(21, 30 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(21, 30 + 1), tempQ1)}


class page4(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses4']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(31, 40 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(31, 40 + 1), tempQ1)}


class page5(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses5']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(41, 50 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(41, 50 + 1), tempQ1)}


class page6(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses6']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(51, 60 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(51, 60 + 1), tempQ1)}

class page7(Page):
    timer_text = 'Time Left:'
    form_model = 'player'
    form_fields = ['myResponses7']

    @staticmethod
    def get_timeout_seconds(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time()

    @staticmethod
    def is_displayed(player: Player):
        return player.participant.vars['expiryPersonality'] - time.time() > 1

    @staticmethod
    def vars_for_template(player: Player):
        tempQ1 = []
        for i in range(61, 66 + 1):
            tempQ1.append(Constants.questions[player.participant.vars['bigFiveOrder'][i] - 1])
        return {'randomQuestionsOrder': zip(range(61, 66 + 1), tempQ1)}

page_sequence = [p01_introduction, page1, page2, page3, page4, page5, page6, page7]
