from otree.api import *


author = 'Yaroslav Rosokha'
doc = """
Informed consent form for Dynamic Power Repeated Game
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_01_Consent'
    players_per_group = None
    num_rounds = 1


class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    consent = models.StringField()


# FUNCTIONS
# PAGES
class Consent(Page):
    form_model = 'player'
    form_fields = ['consent']


class WaitForOthers(WaitPage):
    # template_name = 'informedConsentBehaviorInRepeatedGames/MyWaitPage.html'
    template_name = 'DynamicInequality/MyWaitPage.html'

    @staticmethod
    def vars_for_template(player: Player):
        print("Consent...")
        if player.consent == 'Yes':
            title_text = "Please wait for other participants..."
            body_text = ""
        else:
            title_text = "You may leave the lab now..."
            body_text = ""
        return {'title_text': title_text, "body_text": body_text}


page_sequence = [
    Consent,
    # WaitForOthers
]
