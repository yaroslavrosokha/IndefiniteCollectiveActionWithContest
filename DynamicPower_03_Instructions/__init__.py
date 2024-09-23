from otree.api import *
import numpy as np

author = 'Yaroslav Rosokha & Xinxin Lyu'
doc = """
Dynamic Power experiment description of the payoff tables and transitions.
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_03_Instructions'
    players_per_group = None
    num_rounds = 1
    Belief_c = 10

class Group(BaseGroup):
    pass


class Subsession(BaseSubsession):
    pass


class Player(BasePlayer):
    testingHistory = models.StringField()
    myBelief_firstX = models.IntegerField(min=0, max=100, initial=0, blank=True)
    myBelief_secondX = models.IntegerField(min=0, max=100, initial=0, blank=True)
    myBelief_thirdX = models.IntegerField(min=0, max=100, initial=0, blank=True)

    # myPNorm is the personal norm of my two actions 
    myPNorm_X = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    myPNorm_Y = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    
    # mySNorm is the social norm of my two actions
    mySNorm_X = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    mySNorm_Y = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    
    option1= models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    option2= models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    option3= models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    option4= models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4], blank=True)
    
    stage1Details = models.StringField()
    stage2Details = models.StringField()
    beliefDetails = models.StringField()
    normDetails = models.StringField()
    
    # cal_task1 = models.IntegerField()
    # cal_task2 = models.IntegerField()
    # cal_task3 = models.IntegerField()
    # cal_task4 = models.IntegerField()
    # cal_task5 = models.IntegerField()
    # cal_task6 = models.IntegerField()


# FUNCTIONS
# PAGES
def vars_for_template1(player: Player):
    X0 = player.session.config['Half_Effort_normalized'] * player.session.config['Size']
    
    # player.session.config['Size'] == 2 & player.session.config['Faction_Size'] == 1 :
    string1 = "another participant"
    string2 = "that participant"
    string3 = "the other participant"
    string4 = "the other participant"
    if player.session.config['Size'] == 4 & player.session.config['Faction_Size'] == 1 :
        string1 = "another 3 participants"
        string2 = "those 3 participants"
        string3 = "the other participants"
        string4 = "other participants"
        
    present_total = [0,0,0,0]
    for i in range(player.session.config['Size'] ):
        X = i+1 
        club_production = player.session.config['Benefit']  * X ** player.session.config['kappa'] / (X** player.session.config['kappa'] + X0 ** player.session.config['kappa'])
        ratio = round(1/X, 2) 
        personal_return = round(ratio * club_production + player.session.config['R0'] -  player.session.config['Cost'] )
        presented_total = round((personal_return - 40 )*X)
        present_total[i] = presented_total

    temp = {
        'Faction_Number_minus1':  player.session.config['Size'] - 1,
        'End' : player.session.config['Contest'] == 'endogenous', 
        'matchNumber': "",
        'Payoff': "",
        'Show_label' :  player.session.config['Faction_Size'] == 2 and player.id_in_group > player.session.config['Size'] ,
        'Enable_chat' : player.session.config['Faction_Size'] == 2,
        'FixedRatio' : "{:.0%}".format(player.session.config['Ratio']),
        'Matches': player.session.config['Matches'],
        
        'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),
        'ShowUpFee': int(player.session.config['participation_fee']),
        'CutoffRoll': int(player.session.config['CutoffRoll']),
        
        
        'payoffforDefectionDeductCost' : round(player.session.config['R0'] -  player.session.config['Cost']),
        # Some wordings that will change based on treatments:
        'anotherParticipant' : string1, 
        'thatParticipant' : string2, 
        'theotherParticipant' : string3,         
        'otherParticipants' : string4, 
        
        'action_X_button' :  "<button type='X_button' style='height:30px; width: 30px;' onclick='event.preventDefault()'  > X </button> ",
        'action_Y_button' : "<button type='Y_button' style='height:30px; width: 30px;' onclick='event.preventDefault()'  > Y </button>",
        
        'collectivegood_1C' : present_total[0], 
        'collectivegood_2C' :present_total[1],
        'collectivegood_3C' :  present_total[2],
        'collectivegood_4C' :  present_total[3],
        'payoff_R0' : player.session.config['R0'], 
        'return_example_C2' : round(player.session.config['R0'] -  player.session.config['Cost'] + 0.4 * round(player.session.config['Benefit']  * 2 ** player.session.config['kappa'] / (2** player.session.config['kappa'] + X0 ** player.session.config['kappa'])/2 )*2 ),
        'return_example_C3' : round(player.session.config['R0'] -  player.session.config['Cost'] + 0.4 * round(player.session.config['Benefit']  * 3 ** player.session.config['kappa'] / (3** player.session.config['kappa'] + X0 ** player.session.config['kappa'])/3 )*3 ),
        
        # Additional information for the main experiment:
        'BeliefSCorrectPerRound' : Constants.Belief_c,
        'BeliefSWrongPerRound' : 0,
        # Norm 
        'FixedNormPay' : Constants.Belief_c,
        
        'SocialNormPaya' : 100,
        'SocialNormPayb': 50,
        'SocialNormPayc' : 0,
        'SocialNormPayd' : -50,
        
        'EqualShares' : round(100 / player.session.config['Size']),
        
        
        
        }
    return temp

def js_vars1(player):
        # For each quiz question, this section needs to be manually changed

        # Round number is in this question, how many historical rounds you want to show
        round_number_quiz = 1
        # roll History needs to correspond to the number of rounds
        rollHistory = [1]
        
        
        # Here are the auto part 
        current_title = [ "Current Shares", "Choice", "Earn", "Spend", "Payoff"]
        history_title = [ "Shares", "Choice", "Earn", "Spend","Payoff",]
        
        Num = 5*(round_number_quiz-1)
        
        if player.session.config['Size']  == 2 :
            current_quiz = [current_title, 
                             [50],
                             [50 ],
                             [0],
                             ]
        else :
            current_quiz = [current_title, 
                             [25],
                             [25 ],
                             [25],
                             [25 ],
                             [0],
                             ]
        history_quiz = []
        
        Table_Rearrange = [0 ]
        for i in range(1, player.session.config['Size'] +1):
            Table_Rearrange.append(i)

        
        return dict(
            Faction_Number_minus1 = player.session.config['Size'] - 1,
            matchNumber = "",
            MyID = 1,
            my_id = 1,
            Round = 1,
            
            CutoffRoll = int(player.session.config['CutoffRoll']),
            
            History = history_quiz,
            Current = current_quiz,
            Table_Rearrange = Table_Rearrange,  


            Exo = player.session.config['Contest'] == 'exogenous',
            
            N = player.session.config['Size'],
            x0 = player.session.config['Half_Effort_normalized'],
            kappa = player.session.config['kappa'] ,
            c = player.session.config['Cost'] ,
            r_0 = player.session.config['R0'] , 
            b =  player.session.config['Benefit'] ,
            fixed_ratio = player.session.config['Ratio'],

            
        
        )

def js_vars_quiz(player):
    # The code has 6 rounds, use the first round for quiz question 2 and 3; 4,5,6th round for question 4-6

    # Round number is in this question, how many historical rounds you want to show + 1
    round_number_quiz = 6
    # roll History needs to correspond to the number of rounds; the first is 0 as a placeholder
    rollHistory = [0, 4, 5, 3, 1 , 1]
    
    
    # Here are the auto part 
    current_title = ["Current Shares", "Choice", "Earn", "Spend", "Payoff"]
    history_title = [ "Shares", "Choice", "Earn", "Spend","Payoff",]
    
    Num = 5*(round_number_quiz-1)
    N =  player.session.config['Size']
    X0 = player.session.config['Half_Effort_normalized'] * player.session.config['Size']

    # History example for the four players' choices:
    # Make the effort be a fixed ratio 10% for now 
    Actions = np.matrix([[1,1,0,1,1], [0,0,1,1,1], [0,1,0,1,1], [1,1,1,1,1]])
    Content = np.zeros((N, Num+1))


    Content[:,0] = 1/N * 100
    for r in range(round_number_quiz-1) : 
        # r is the round number, starting from round 1, r= 0
        action_column = 5*r + 1
        Content[:,action_column]=Actions[0:N, r].flatten()
        X = Content[:,action_column].sum()
        CollectiveGood =  player.session.config['Benefit']  * X** player.session.config['kappa'] / (X** player.session.config['kappa'] + X0 ** player.session.config['kappa'])

       # Calculate power
        power =  np.round(np.multiply(Content[:,5*r], Content[:,5*r+1]).sum(),2)
        if power != 0 :
            Content[:, 5*r+2] = np.round(player.session.config['R0'] + np.multiply(np.round(Content[:,5*r]/ power,2), Content[:,5*r+1]) * CollectiveGood  - Content[:,5*r+1] * player.session.config['Cost'])
        else :
            Content[:, 5*r+2] =np.round( [player.session.config['R0']]*player.session.config['Size'])
        
        # Effort column
        Content[:, 5*r+3] = np.round(player.session.config['Ratio'] * Content[:, 5*r+2])
        Content[:, 5*r+4] = np.round((1- player.session.config['Ratio']) * Content[:, 5*r+2])
        # print( np.round(Content[:, 5*r+3] /  Content[:, 5*r+3].sum(),2) * 100)
        Content[:, 5*r+5] = [ str("%.2f" % x) for x in  np.round(Content[:, 5*r+3] /  Content[:, 5*r+3].sum(),2) * 100]
    
    # For quiz 2,
    if player.session.config['Size'] == 2 :
        history_quiz = [ history_title* (round_number_quiz-1),
                        Content[0, 0:-1].tolist(),
                        Content[1, 0:-1].tolist(),
                        rollHistory, ]
        current_quiz = [current_title, 
                        [Content[0, Num]],
                        [Content[1, Num]],
                         [0],
                         ]
    else : 
        history_quiz = [ history_title*(round_number_quiz-1),
                        Content[0, 0:-1].tolist(),
                        Content[1, 0:-1].tolist(),
                        Content[2, 0:-1].tolist(),
                        Content[3, 0:-1].tolist(),
                        rollHistory, ]

        current_quiz = [current_title, 
                        [Content[0, Num]],
                        [Content[1, Num]],
                        [Content[2, Num]],
                        [Content[3, Num]],
                         [0],
                         ]
    
    
    Table_Rearrange = [0 ]
    for i in range(1, player.session.config['Size'] +1):
        Table_Rearrange.append(i)

    
    return dict(
        Faction_Number_minus1 = player.session.config['Size'] - 1,
        matchNumber = "",
        MyID = 1,
        my_id = 1,
        Round = round_number_quiz,
        
        CutoffRoll = int(player.session.config['CutoffRoll']),
        
        History = history_quiz,
        Current = current_quiz,
        Table_Rearrange = Table_Rearrange,  
        # Content = Content,

        Exo = player.session.config['Contest'] == 'exogenous',
        
        N = player.session.config['Size'],
        x0 = player.session.config['Half_Effort_normalized'],
        kappa = player.session.config['kappa'] ,
        c = player.session.config['Cost'] ,
        r_0 = player.session.config['R0'] , 
        b =  player.session.config['Benefit'] ,
        fixed_ratio = player.session.config['Ratio'],
    )
    
class WaitForOthers(WaitPage):

    @staticmethod
    def vars_for_template(player: Player):
        title_text = ""
        body_text = "Please wait for other participants to finish Part 1."
        return {'title_text': title_text, "body_text": body_text}

        
class P01_BeginPart2(Page):
    vars_for_template = vars_for_template1

class P02_MatchWork(Page):
    form_model = 'player'
    form_fields = ['testingHistory']

    vars_for_template = vars_for_template1

        
class P03_RoundOverview(Page):

    vars_for_template = vars_for_template1


class P04a_Stage1Details(Page):
    form_model = 'player'


    vars_for_template = vars_for_template1
    js_vars = js_vars1


class P04b_Stage1Details(Page):
    form_model = 'player'
    form_fields = ['stage1Details']


    vars_for_template = vars_for_template1
    js_vars = js_vars1



class P05a_Stage2Details(Page):
    vars_for_template = vars_for_template1
    def js_vars(player):
        d = js_vars_quiz(player)
        # Here only want to show the first round history_quiz
                     
        round_number_quiz = 1
        Num = 3
        
        
        # For quiz 2, first round, only define the current table
        history_quiz = []
        
        if player.session.config['Size'] == 2 :
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:Num], ]
        else : 
            current_quiz =  [ d['Current'][0][0:5],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:Num],]

        
           
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
       
        
        return dict(d,
                    )   


class P05b_Stage2Details(Page):
    form_model = 'player'
    form_fields = ['stage2Details']
    
    vars_for_template = vars_for_template1
    def js_vars(player):
        d = js_vars_quiz(player)
        # Here only want to show the first round history_quiz
                     
        round_number_quiz = 1
        Num = 3
        
        # For quiz 2, first round, only define the current table
        history_quiz = []
        if player.session.config['Size'] == 2 :
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:Num], ]
        else : 
            current_quiz =  [ d['Current'][0][0:5],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:Num],]

        
           
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
       
        
        return dict(d,
                    )    

                    
class P06_Calculator(Page) :

    # form_model = 'player'
    # form_fields =  [cal_task1, cal_task2, cal_task3, cal_task4, cal_task5, cal_task6]

    vars_for_template = vars_for_template1
    
    js_vars = js_vars1
    
class P07_History(Page):
    vars_for_template = vars_for_template1
    
    
    @staticmethod
    def js_vars(player):
        # For each quiz question, this section needs to be manually changed

        # Round number is in this question, how many historical rounds you want to show + 1
        round_number_quiz = 4
        # roll History needs to correspond to the number of rounds; the first is 0 as a placeholder
        rollHistory = [0, 4, 5, 3]
        
        d = js_vars_quiz(player)
        
                     
        Num = (round_number_quiz-1)*5 
        if player.session.config['Size'] == 2 :
            history_quiz = [d['History'][0][0:Num],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:round_number_quiz],]
                            
            current_quiz = [ d['Current'][0][0:5],
                            [d['History'][1][Num]],
                           [d['History'][2][Num]],
                            [d['History'][3][round_number_quiz]], ]
        else : 
            history_quiz = [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:round_number_quiz],]
            current_quiz =  [ d['Current'][0][0:5],
                            [d['History'][1][Num]],
                            [d['History'][2][Num]],
                            [d['History'][3][Num]], 
                            [d['History'][4][Num]],
                            [d['History'][5][round_number_quiz]],]

        
           
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
       
        
        return dict(d,
                    )    

        
        

class P08_AdditionalQuestions(Page) :
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
        
    vars_for_template = vars_for_template1
 
class P09_BeliefElicitation(Page):
    template_name = 'DynamicPower_03_Instructions/P09_BeliefElicitation.html' 
    form_model = 'player'
    form_fields = ['beliefDetails']
    @staticmethod
    def get_form_fields(player: Player):
        if player.session.config['Size'] >2: 
            return ['myBelief_firstX',
                    'myBelief_secondX', 
                    'myBelief_thirdX']
        else:
            return ['myBelief_firstX']
        
        
    vars_for_template = vars_for_template1
    
class P10_PersonalNormElicitation(Page):
    template_name = 'DynamicPower_03_Instructions/P10_PersonalNormElicitation.html' 

    form_model = 'player'
    form_fields = ['myPNorm_X', 'myPNorm_Y']
       
    vars_for_template = vars_for_template1

class P11_SocialNormElicitation(Page):
    template_name = 'DynamicPower_03_Instructions/P11_SocialNormElicitation.html' 

    form_model = 'player'
    form_fields = ['mySNorm_X', 'mySNorm_Y', 'option1', 'option2', 'option3', 'option4','normDetails']
   
    vars_for_template = vars_for_template1    
   


page_sequence = [
    WaitForOthers,
    P01_BeginPart2,
    P02_MatchWork,
    P03_RoundOverview,
    P04a_Stage1Details,
    P04b_Stage1Details,
    P05a_Stage2Details,
    P05b_Stage2Details,
    P06_Calculator,
    P07_History,
    P08_AdditionalQuestions, 
    P09_BeliefElicitation,
    P10_PersonalNormElicitation,
    P11_SocialNormElicitation,


]
