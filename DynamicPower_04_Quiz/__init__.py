import copy as cp

import numpy as np
from otree.api import *


author = 'Yaroslav Rosokha & Xinxin Lyu'
doc = """
A quiz app for dynamic power repeated games experiment.
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicPower_04_Quiz'
    players_per_group = None
    num_rounds = 1



class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    quiz1_D = models.IntegerField()
    # quiz1_AllC = models.IntegerField()
    quiz1_1C= models.IntegerField()
    quiz2 = models.IntegerField()
    quiz3 = models.FloatField()
    quiz4 = models.IntegerField()
    quiz5 = models.FloatField()
    quiz6 = models.IntegerField()
    
    quizHistory1 = models.StringField()
    quizHistory2 = models.StringField()
    quizHistory3 = models.StringField()
    quizHistory4 = models.StringField()
    quizHistory5 = models.StringField()
    quizHistory6 = models.StringField()
    quizHistory7 = models.StringField()
    quizHistory8 = models.StringField()
    quizHistory9 = models.StringField()
    quizHistory10 = models.StringField()

# FUNCTIONS
# PAGES

def vars_for_template1(player: Player):
    X0 = player.session.config['Half_Effort_normalized'] * player.session.config['Size']
    
    # if player.session.config['Size'] == 2 and player.session.config['Faction_Size'] == 1 :
    string1 = "another participant"
    string2 = "that participant"
    string3 = "the other participant"
    string4 = "the other participant chooses"
    if player.session.config['Size'] == 4 and player.session.config['Faction_Size'] == 1 :
        string1 = "another 3 participants"
        string2 = "those 3 participants"
        string3 = "the other participants"
        string4 = "all other participants choose"
        
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
        
        'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),
        'ShowUpFee': int(player.session.config['participation_fee']),
        'CutoffRoll': int(player.session.config['CutoffRoll']),
        
        
        'payoffforDefectionDeductCost' : round(player.session.config['R0'] -  player.session.config['Cost']),
        # Some wordings that will change based on treatments:
        'anotherParticipant' : string1, 
        'thatParticipant' : string2, 
        'theotherParticipant' : string3,     
        'theotherParticipantChooses' : string4,     
            
        
        'action_X_button' :  "<button type='X_button' style='height:30px; width: 30px;' onclick='event.preventDefault()'  > X </button> ",
        'action_Y_button' : "<button type='Y_button' style='height:30px; width: 30px;' onclick='event.preventDefault()'  > Y </button>",
        
        'collectivegood_1C' : present_total[0], 
        'collectivegood_2C' :present_total[1],
        'collectivegood_3C' :  present_total[2],
        'collectivegood_4C' :  present_total[3],        'return_example_C2' : round(player.session.config['R0'] -  player.session.config['Cost'] + 0.4 * round(player.session.config['Benefit']  * 2 ** player.session.config['kappa'] / (2** player.session.config['kappa'] + X0 ** player.session.config['kappa'])/2 )*2 ),
        'return_example_C3' : round(player.session.config['R0'] -  player.session.config['Cost'] + 0.4 * round(player.session.config['Benefit']  * 3 ** player.session.config['kappa'] / (3** player.session.config['kappa'] + X0 ** player.session.config['kappa'])/3 )*3 ),
        }
    return temp
    

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
    Actions = np.matrix([[0,1,0,1,1], [1,1,0,1,1], [1,0,1,1,1], [1,0,0,0,1]])
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

def js_vars_initial(player):
        # Round number is in this question, how many historical rounds you want to show
        round_number_quiz = 1
        # roll History needs to correspond to the number of rounds
        rollHistory = [1]
        
        
        # Here are the auto part 
        current_title = ["Current Shares", "Choice", "Earn", "Spend", "Payoff"]
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
            
        N =  player.session.config['Size']
        X0 = player.session.config['Half_Effort_normalized'] * player.session.config['Size']    
        quiz1_solutions = [ player.session.config['R0'], ]
        for X in range(1, player.session.config['Size'] +1) :
            CollectiveGood =  player.session.config['Benefit']  * X** player.session.config['kappa'] / (X** player.session.config['kappa'] + X0 ** player.session.config['kappa'])
            payoff =  np.round(player.session.config['R0'] + 1/X * CollectiveGood  -  player.session.config['Cost'])
            quiz1_solutions.append(payoff)
        

        Table_Rearrange = [0 ]
        for i in range(1, player.session.config['Size'] +1):
            Table_Rearrange.append(i)

        
        d = dict(
            Faction_Number_minus1 = player.session.config['Size'] - 1,
            matchNumber = "",
            MyID = 1,
            my_id = 1,
            Round = round_number_quiz,
            
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
            
            quiz1_D= quiz1_solutions[0],
            quiz1_1C= quiz1_solutions[1],
            quiz1_2C= quiz1_solutions[2],
            quiz1_AllC = quiz1_solutions[-1],
            error_message = "This is incorrect. If you have questions, please raise your hand. The correct answer is: ",


        )
        
        if player.session.config['Size'] > 2 :
            d['quiz1_3C'] = quiz1_solutions[3]
            d['quiz1_4C'] = quiz1_solutions[4]
            return dict(d , 
                    quiz1_3C= quiz1_solutions[3],
                    quiz1_4C= quiz1_solutions[4])
        else :
            return dict( d )
            
            
            
class beginQuiz(Page):
    pass


class Question1_2(Page):
    # This question is for same power, payoff 
    form_model = 'player'
    # Double check to makes sure 1C is correct!!
    form_fields =  ['quizHistory1','quiz1_D','quiz1_1C']

            
            
    vars_for_template = vars_for_template1
    js_vars = js_vars_initial
    
    
    

class Question3(Page):
    form_model = 'player'
    form_fields = ['quizHistory2', 'quiz2']

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

        if player.session.config['Contest'] == 'exogenous' :
            error_m = "This is incorrect. If you have questions, please raise your hand. The correct answer is: "
            quiz2 = d['History'][1][Num-1] * player.session.config['Ratio']
        else :
            error_m = "This is incorrect. If you have questions, please raise your hand. The correct answer is: "
            quiz2 = d['History'][1][Num-1] 
        
           
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
        
        return dict(d,
                    error_message =  error_m,
                    quiz2 = quiz2, 
                    )
        
class Question4(Page):
    form_model = 'player'
    form_fields = ['quizHistory3', 'quiz3']

    vars_for_template = vars_for_template1
    
    def js_vars(player):        
        
        if player.session.config['Size'] == 2 :
            quiz3 = 40
        else :
            quiz3 = 20
            
        error_m = "This is incorrect. If you have questions, please raise your hand. The correct answer is: "
        
                       
        d = js_vars_quiz(player)
        # Here only want to show the first round history_quiz
                     
        round_number_quiz = 1
        Num = 3
        
        
        # For quiz 2, first round, only define the current table
        history_quiz = []
       
        if player.session.config['Size'] == 2 :
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][5:5+Num],
                           d['History'][2][5:5+Num],
                            d['History'][3][5:5+Num], ]
        else : 
            current_quiz =  [ d['Current'][0][0:5],
                            d['History'][1][5:5+Num],
                            d['History'][2][5:5+Num],
                            d['History'][3][5:5+Num], 
                            d['History'][4][5:5+Num],
                            d['History'][5][5:5+Num],]
        
           
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
        
        return dict(d,
                    quiz3 = quiz3, 
                    error_message =  error_m,
                     
                    )
                    
                    
                    
                    
        
class Question5_7(Page):
    form_model = 'player'
    form_fields = ['quizHistory4',  'quiz5', 'quiz6']
    
    vars_for_template = vars_for_template1
    
    
    def js_vars(player):
        d = js_vars_quiz(player)
        # Here we want to show the 4th round history_quiz (total 5)
                     
        round_number_quiz = 4
        Num = 5*(round_number_quiz-1)
        
        
        # For quiz 5-7, first round, only define the current table
        if player.session.config['Size'] == 2 :
            history_quiz = [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:round_number_quiz], ]
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+3],
                           d['History'][2][Num:Num+3],
                            [], ]
            effort_input = [ d['History'][1][Num+3] , d['History'][2][Num+3] ]
        else : 
            history_quiz =  [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:round_number_quiz],]

            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+3],
                            d['History'][2][Num:Num+3],
                            d['History'][3][Num:Num+3], 
                            d['History'][4][Num:Num+3],
                            [],]
            effort_input = [ d['History'][1][Num+3],
                                d['History'][2][Num+3],
                                d['History'][3][Num+3],
                                d['History'][4][Num+3] ]
            
        
        # quiz4 = d['History'][1][Num+2]
        quiz5 = round(d['History'][1][Num+5], 2)
        quiz6 =  d['History'][1][Num+7]
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
        
       
        return dict(d,
                error_message = "This is incorrect. If you have questions, please raise your hand. The correct answer is: ",
                    # quiz4 = quiz4, 
                    quiz5 = quiz5, 
                    quiz6 = quiz6, 
                    effort_input = effort_input,
                    )
        

class Question8(Page):
    form_model = 'player'
    form_fields = ['quizHistory7']

    vars_for_template = vars_for_template1
    
    
    def js_vars(player):
        d = js_vars_quiz(player)
        # Here we want to show the 4th round history_quiz (total 5)
                     
        round_number_quiz = 4
        Num = 5*(round_number_quiz-1)
        
        
        # For quiz 2, first round, only define the current table
        if player.session.config['Size'] == 2 :
            history_quiz = [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:round_number_quiz], ]
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+3],
                           d['History'][2][Num:Num+3],
                            [], ]
        else : 
            history_quiz =  [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:round_number_quiz],]

            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+3],
                            d['History'][2][Num:Num+3],
                            d['History'][3][Num:Num+3], 
                            d['History'][4][Num:Num+3],
                            [],]
        
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
        
       
        return dict(d,
                    )

class Question9(Page):
    form_model = 'player'
    form_fields = ['quizHistory8']

    vars_for_template = vars_for_template1
    def js_vars(player):
        d = js_vars_quiz(player)
        # Here we want to show the 4th round history_quiz (total 5)
                     
        round_number_quiz = 4
        Num = 5*(round_number_quiz-1)
        
        
        # For quiz 2, first round, only define the current table
        if player.session.config['Size'] == 2 :
            history_quiz = [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                           d['History'][2][0:Num],
                            d['History'][3][0:round_number_quiz], ]
            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+2],
                           d['History'][2][Num:Num+2],
                            [], ]
        else : 
            history_quiz =  [ d['History'][0][0:Num],
                            d['History'][1][0:Num],
                            d['History'][2][0:Num],
                            d['History'][3][0:Num], 
                            d['History'][4][0:Num],
                            d['History'][5][0:round_number_quiz],]

            current_quiz = [ d['Current'][0][0:5],
                            d['History'][1][Num:Num+2],
                            d['History'][2][Num:Num+2],
                            d['History'][3][Num:Num+2], 
                            d['History'][4][Num:Num+2],
                            [],]
        
        d['Round'] = round_number_quiz
        d['History'] = history_quiz
        d['Current'] = current_quiz
        
       
        return dict(d,
                    )


class Question10(Page):
    form_model = 'player'
    form_fields = ['quizHistory9']

    vars_for_template = vars_for_template1


class Question11(Page):
    form_model = 'player'
    form_fields = ['quizHistory10']

    @staticmethod
    def vars_for_template(player: Player):
        temp = {
            'rollHistory': ",1,1,1,3,2",
            'roundHistory': ",1,2,3,4,5",
            'tableRandomNumberHistory': ",2,2,4,2,4",
            'tableNumberHistory': ",2,2,4,3,4",
            'myChoiceHistory': ",0,1,1,1,0",
            'otherChoiceHistory': ",1,0,0,1,0",
            'myPayoffHistory': ",25,12,12,32,25",
            'otherPayoffHistory': ",12,25,50,32,25",
            'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),
            'ShowUpFee': int(player.session.config['participation_fee']),
            'CutoffRoll': int(player.session.config['CutoffRoll']),
        }
        return temp


class p01_WaitForGroup(WaitPage):
    template_name = 'DynamicPower_04_Quiz/p01_WaitForGroup.html'

    @staticmethod
    def after_all_players_arrive(group: Group):
        pass

    @staticmethod
    def vars_for_template(player: Player):
        temp = {'matchNumber': 1}
        return temp


page_sequence = [
    beginQuiz,
    Question1_2,
    Question3,
    # Question4,
    # Question5_7,
    Question8,
    Question9,
    Question10,
    Question11,
]
