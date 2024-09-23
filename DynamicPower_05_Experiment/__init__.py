import copy as cp

import numpy as np
from otree.api import *
def Convert(string): 
    list1=[] 
    list1[:0]=string 
    return list1 


# code based on author = 'Yaroslav Rosokha December 2019' DynamicQueue_05_Experiment
author = 'Xinxin Lyu / Yaroslav Rosokha / 2020'
                          
doc = """
Dynamic Power Experiment
"""


class Constants(BaseConstants):
    name_in_url = 'DynamicInequality_Experiment_main'
    
    
    seqs10 = [
        [4, 2, 3, 2, 9, 11, 3, 4, 2, 19, 11, 35, 2, 5, 8, 5, 2, 10, 27, 6],
        [9, 6, 21, 5, 3, 7, 12, 5, 5, 12, 18, 7, 7, 17, 5, 2, 48, 4, 2, 9],
        [16, 4, 9, 11, 18, 21, 2, 3, 14, 2, 6, 22, 13, 9, 3, 9, 7, 6, 18, 17],
        [2, 7, 36, 41, 2, 5, 7, 12, 3, 18, 2, 21, 2, 1, 1, 5, 6, 2, 9, 1], 
        [9, 10, 21, 16, 4, 3, 9, 40, 3, 35, 11, 46, 4, 17, 1, 31, 3, 4, 4, 1], 
        ]

    # num_rounds = int(np.max([np.max(np.sum(seqs10, axis=1)), 125]))
    # First 10 matches: [59, 85, 100, 133, 150]
    # 20 matches : [170, 204, 210, 183, 272]
    
    num_rounds = 272
    
    cumul10 = [np.roll(np.cumsum(s, dtype=int), 1) for s in seqs10]
    # Maybe: the sequence number
    #num_rounds = cumul10[s][0]
    # Since Constants does not have access to the session config,
    # (it is loaded when the server starts, rather than for each session)
    # we set the groups manually inside creating_session.
    players_per_group = None
    # Put into the payoff stage
    # Assign different roles, can't use the constant to define any more
    # if self.config['Faction_Size'] == "individual" :
    # players_per_group = self.config['Size']
    # Plan for 'Faction' = "group" , within group, different type (type A vs B), each group has 2 subjects
    # else :
    # players_per_group = 2 * self.config['Size']   
    
    # BeliefSCorrectPerRound
    Belief_c = 10
    
    


class Subsession(BaseSubsession):
    pass

class Group(BaseGroup):
    matchNumber = models.IntegerField(initial=0)
    roundNumber = models.IntegerField(initial = 0)
    roundHistory = models.StringField(initial="0")

    public_output = models.CurrencyField(initial = 0)
    total_contribution = models.IntegerField(initial = 0)
    total_power = models.FloatField(min=0, max=1)
    total_effort = models.CurrencyField(initial=0)
    
    round_line = models.StringField(initial = "-1")
    title_line = models.StringField(initial = "-1")
    first_line = models.StringField(initial = "-1")
    second_line = models.StringField(initial = "-1")
    third_line = models.StringField(initial = "-1")
    fourth_line = models.StringField(initial = "-1")
    
    # For live message, should only be changed when the Faction == 'Group'
    members_decided = models.StringField(initial = "-1")



class Player(BasePlayer):
    # Variables can be kept
    ## myChoice is a dummy for cooperate or not; 0 = not cooperate, 1= cooperate
    myChoice = models.IntegerField(initial=-1)
    ## myPayoff excludes the earnings from belief elicitation
    myPayoff = models.CurrencyField(initial = 0)
    roundPayoff = models.CurrencyField(initial = 0)
    matchPayoff = models.CurrencyField(initial = 0)
    roll = models.IntegerField(initial = 0)
    myChoiceHistory = models.StringField(initial = "-1")
    # otherChoiceHistory = models.StringField()
    myPayoffHistory = models.StringField(initial = "-1")
    # otherPayoffHistory = models.StringField()
    rollHistory = models.StringField(initial="0")
    # Variables added
    # myPower is between [0,1] for individual political power
    myPower = models.FloatField(min=0, max=1)
    myNextPower = models.FloatField(min=0, max=1)
    # myBelief is the elicitated beliefs of cooperating others\
    myBelief_firstX = models.IntegerField(min=0, max=100, initial=-1)
    myBelief_secondX = models.IntegerField(min=0, max=100, initial=-1)
    myBelief_thirdX = models.IntegerField(min=0, max=100, initial=-1)
    # Added social norm fixed pay in the function          
    myBelief_payoff = models.CurrencyField(initial = 0)

    # myPNorm is the personal norm of my two choices 
    myPNorm_X = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4])
    myPNorm_Y = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4])
    
    # mySNorm 
    mySNorm_X = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4])
    mySNorm_Y = models.IntegerField(widget=widgets.RadioSelect, choices=[1,2,3,4])


    # myEffort is the effort each faction put in the contest/for next round power
    myEffort = models.FloatField(initial = 0, min=0)
    myPowerHistory = models.StringField(initial = "-1")
    myEffortHistory = models.StringField(initial = "-1")
    lineHistory = models.StringField(initial = "-1")
    matchNumber = models.IntegerField(initial=0)
    
    channel_str  = models.StringField(initial = "-1")
    chat_nickname = models.StringField(initial = "-1")
    
    
    calculatorHistory0 = models.StringField()
    calculatorHistory2 = models.StringField()
    calculatorHistory3 = models.StringField()
    calculatorHistory4 = models.StringField()
    calculatorHistory5 = models.StringField()
    calculatorHistory6 = models.StringField()
    calculatorHistory7 = models.StringField()
    calculatorHistory8 = models.StringField()
    calculatorHistory9 = models.StringField()



def myEffort_max(player):
    return float(player.myPayoff)
    
def myEffort_error_message(player, value):
    print('value is', value)
    if value > float(player.myPayoff):
        return 'Cannot compete more than your earnings'
    
# FUNCTIONS
def creating_session(subsession: Subsession):
    if subsession.session.config['Faction_Size'] == 1 :
        ppg = subsession.session.config['Size']

    elif subsession.session.config['Faction_Size'] == 2:
        ppg = subsession.session.config['Size'] * 2
        # Note: when the faction consists multiple subjects, can add roles in the group
        
    players = subsession.get_players()
    matrix = []
    for i in range(0, len(players), ppg):
        matrix.append(players[i : i + ppg])
    subsession.set_group_matrix(matrix)
    
    
    seq_id = subsession.session.config['Sequence'] - 1
    if subsession.session.config['CutoffRoll'] == 10:
        crit_rounds = Constants.cumul10[seq_id]
    crit_rounds[0] = 0
    if subsession.round_number - 1 in crit_rounds:
        subsession.group_randomly()
    else:
        subsession.group_like_round(subsession.round_number - 1)

        
        
def get_contribution_outcomes(group: Group):
    
    total_contribution = 0
    total_power = 0
    X0 = group.session.config['Half_Effort_normalized'] * group.session.config['Size']
    
    for p in group.get_players():
        if p.id_in_group <= group.session.config['Size']: 
            total_contribution += p.myChoice
            if p.myChoice == 1:
                total_power += p.myPower
                
    group.total_contribution = total_contribution
    group.public_output = group.session.config['Benefit']  * group.total_contribution** group.session.config['kappa'] / (group.total_contribution** group.session.config['kappa'] + X0 ** group.session.config['kappa'])
    group.total_power = total_power
    for p in group.get_players():
        if p.myChoice == 1:
            if total_power == 0 :
                x = round(1/total_contribution, 2)
            else :
                x = round(p.myPower / total_power, 2)
            p.myPayoff = round(group.session.config['R0'] + group.public_output * x - group.session.config['Cost'])
        elif  p.myChoice == 0:
            p.myPayoff = round(group.session.config['R0'])
        p.lineHistory += "," + str(p.myPayoff)
    update_table_content(group)


def get_belief_outcomes(group: Group) :
    import random
    choice_list = []
    for p in group.get_players():
        # Firstly, get the choice within group:
        choice_list.append(p.myChoice)
        
    # Secondly, compare each subject's belief with the real choice:
    for p in group.get_players():
        myID = p.id_in_group % p.session.config['Size'] 
        if myID == 0:
            myID =  p.session.config['Size'] 
        if p.session.config['Size'] == 2: 
            myAnswer = [p.myBelief_firstX]
        else :
            myAnswer = [p.myBelief_firstX, p.myBelief_secondX, p.myBelief_thirdX] 
        
        
        if p.myBelief_firstX == -1 :
            p.myBelief_payoff = 0
        
        else :
            ToCompare = [ x for i, x in enumerate(choice_list) if i!= myID-1]        
            Determine = 0 
            if  p.session.config['Size']  == 2 :
                prob =  1- (((1-ToCompare[0])*100 - myAnswer[0] )/100 )** 2 
                Determine  +=  (random.random() <= prob ) *1
            else :
                for x,y in zip(ToCompare, myAnswer) :
                    prob =  1- ((1-x)*100 - y )** 2 
                    Determine  +=  (random.random() <= prob ) *1
            # Added social norm fixed pay here         
            
            p.myBelief_payoff = Determine * Constants.Belief_c + 2 * Constants.Belief_c
            



def get_competition_outcomes(group: Group):
    total_effort = 0
    for p in group.get_players():
        if p.id_in_group <= group.session.config['Size']: 
            total_effort += p.myEffort
        else:
                    
            decider_number = p.id_in_group % group.session.config['Size'] 
            if decider_number == 0 :
                p.myEffort = group.get_player_by_id(group.session.config['Size']).myEffort
            else :
                p.myEffort = group.get_player_by_id(decider_number).myEffort
                    
                    
                    
                    
    group.total_effort = total_effort

    
    for p in group.get_players():
        p.roundPayoff = p.myPayoff - p.myEffort
        p.payoff = p.myPayoff - p.myEffort + p.myBelief_payoff
        p.matchPayoff += p.payoff 

        
        seq_id = group.session.config['Sequence'] - 1
        if group.session.config['CutoffRoll'] == 10:
            crit_rounds = Constants.cumul10[seq_id]
        if group.round_number in crit_rounds:
            temp_roll = np.random.choice(list(range(group.session.config['CutoffRoll'], 11)))
            p.roll = int(temp_roll)
        else:
            temp_roll = np.random.choice(list(range(1, group.session.config['CutoffRoll'])))
            p.roll = int(temp_roll)
        
        if float(total_effort) != 0 :
            p.myNextPower = round( float(p.myEffort) / float(p.group.total_effort), 2)
        else:
            p.myNextPower = round( 1 / p.session.config['Size'], 2)

        update_history(p)
        p.lineHistory += "," + str(round(p.roundPayoff))
        
    update_table_content(group)

def update_table_content(group: Group):
    group.first_line = group.get_player_by_id(1).lineHistory
    group.second_line = group.get_player_by_id(2).lineHistory
    
    if group.session.config['Size'] > 2:
        group.third_line = group.get_player_by_id(3).lineHistory
        group.fourth_line = group.get_player_by_id(4).lineHistory



def get_role(group: Group):
    
    for p in group.get_players() :
        residual = p.id_in_group % p.session.config['Size']

        p.channel_str = str(p.group.id) + str(residual)
        if p.id_in_group <= group.session.config['Size']:
            p.chat_nickname = "Decider"
        else :
            p.chat_nickname = "Non Decider"

 
                
def init_match(player: Player):
    player.myPower = 1 / player.session.config['Size']
    player.lineHistory = str(player.myPower*100)


def init_round(player: Player):
    
    
    player.rollHistory = player.in_round(player.round_number - 1).rollHistory
    player.matchPayoff = player.in_round(player.round_number - 1).matchPayoff
    
    # This is where the political power will be updated
    player.myPower = round(player.in_round(player.round_number - 1).myNextPower, 2)
    
    
    player.lineHistory = player.in_round(player.round_number - 1).lineHistory + ","+ str("%.2f" % round(player.myPower*100,2))

def update_history(player: Player):
    player.rollHistory += "," + str(player.roll)
    player.myChoiceHistory += "," + str(player.myChoice)
    player.myPayoffHistory += "," + str(player.myPayoff)
    # Variables added
    player.myPowerHistory += "," + str("%.2f" % round(player.myPower*100,2))
    player.myEffortHistory += "," + str("%.2f" % round(player.myEffort,0)) 
    

# def chat_channel(player: Player):
    # group = player.group
    # channel_number = player.id_in_group

    # return 'Group {} player {}'.format(group.id_in_subsession, player.id_in_group)


#---------------------------------------------------------------------------------#
# PAGES
#---------------------------------------------------------------------------------#
def vars_for_admin_report(subsession):
    pid = sorted([p.id_in_subsession for p in subsession.get_players()])
    payoffs = sorted([p.payoff for p in subsession.get_players()])
    matches = sorted([p.group.matchNumber for p in subsession.get_players()])
    rounds =  sorted([p.group.roundNumber for p in subsession.get_players()])
    table_output = sorted([[p.id_in_subsession, p.group.matchNumber, p.group.roundNumber, p.payoff, p.matchPayoff]  for p in subsession.get_players()])
    return dict(
                table_output = table_output,
                payoffs=payoffs,
                matches = matches, 
                rounds = rounds,
                
                )

def is_displayed1(player: Player):
    # ''' For all rounds before the last round''' 
    seq_id = player.session.config['Sequence'] - 1
    if player.session.config['CutoffRoll'] == 10:
        total_rounds = np.sum(Constants.seqs10[seq_id][0:player.session.config['Matches']])
    return player.round_number <= total_rounds
    
def is_displayed2(player: Player):
    # ''' For the first and last match (belief and personal norm) '''
    # Must be after page: WaitForGroup (where we created the group.matchNumber
    
    return  player.group.matchNumber ==  1 or player.group.matchNumber== player.session.config['Matches'] or player.group.matchNumber== 10

def vars_for_template1(player: Player):
    string3 = "the other participant"
    if player.session.config['Size'] == 2 & player.session.config['Faction_Size'] == 1 :
        string3 = "the other participants"


    temp = {
        'Faction_Number_minus1':  player.session.config['Size'] - 1,
        'CutoffRoll' : int(player.session.config['CutoffRoll']),

        'matchNumber': player.group.matchNumber,
        'Payoff': player.myPayoff,
        'Show_label' :  player.session.config['Faction_Size'] == 2 and player.id_in_group > player.session.config['Size'] , 
        'Enable_chat' : player.session.config['Faction_Size'] == 2,
        
        'theotherParticipant' : string3,      
        
    }
    return temp


def js_vars1(player):
        Num = 5*(player.group.roundNumber-1)
        rollHistory = [int(x) for x in player.rollHistory.split(",")]
        title_line = [x for x in player.group.title_line.split(",")]
        first_line = [float(x) for x in player.group.first_line.split(",")]
        second_line =  [float(x) for x in player.group.second_line.split(",")]
        third_line = [float(x) for x in player.group.third_line.split(",")]
        fourth_line = [float(x) for x in player.group.fourth_line.split(",")]
        
        
        History_block = []
        Current_block = []
        if player.session.config['Size']==2 :
            Current_block = [title_line[Num::], first_line[Num::], second_line[Num::], rollHistory[player.group.roundNumber-1]]
            if Num >0 :
                History_block = [title_line[0:Num], first_line[0:Num], second_line[0:Num], rollHistory[0:player.group.roundNumber]]
        elif player.session.config['Size']==4 :    
            Current_block = [title_line[Num::], first_line[Num::], second_line[Num::],third_line[Num::], fourth_line[Num::], rollHistory[player.group.roundNumber-1]]
            if Num >0 :
                History_block = [title_line[0:Num], first_line[0:Num], second_line[0:Num], third_line[0:Num], fourth_line[0:Num], rollHistory[0:player.group.roundNumber]]
        
        myID = player.id_in_group % player.session.config['Size'] 
        if myID == 0:
            myID =  player.session.config['Size'] 
            
        Table_Rearrange = [0, myID ]
        for i in range(1, player.session.config['Size'] +1):
            if i != myID :
                Table_Rearrange.append(i)
        
        
        
        return dict(
            Faction_Number_minus1 = player.session.config['Size'] - 1,
            matchNumber = player.group.matchNumber,
            MyID = myID,
            my_id = player.id_in_group,
            Round = player.group.roundNumber,
            
            CutoffRoll = int(player.session.config['CutoffRoll']),
            Power = player.myPower * 100    ,
            Effort = player.myEffort,
            Payoff = player.myPayoff,
            rollHistory = player.rollHistory,
            
            title_line =  player.group.title_line,
            round_line = player.group.round_line,
            first_line =  player.group.first_line,
            second_line = player.group.second_line,
            third_line = player.group.third_line,
            fourth_line = player.group.fourth_line,
            
            History = History_block,
            Current = Current_block,
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

class P00_WaitForOthers(WaitPage):

    wait_for_all_groups = True
    
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1
        

    template_name = 'DynamicPower_05_Experiment/P00_WaitForOthers.html'

    form_model = 'player'
    form_fields = ['calculatorHistory0']

    
    vars_for_template = vars_for_template1
    
    @staticmethod
    def js_vars(player):
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


                Exo = player.session.config['Contest'] == 'exogenous',
                
                N = player.session.config['Size'],
                x0 = player.session.config['Half_Effort_normalized'],
                kappa = player.session.config['kappa'] ,
                c = player.session.config['Cost'] ,
                r_0 = player.session.config['R0'] , 
                b =  player.session.config['Benefit'] ,
                fixed_ratio = player.session.config['Ratio'],
               

            )
                   


class P01_beginExperiment(Page):
    @staticmethod
    def is_displayed(player: Player):
        return player.round_number == 1

    @staticmethod
    def vars_for_template(player: Player):
        return {
            'Matches': player.session.config['Matches'],
            'PointsPerDollar': int(1.0 / player.session.config['real_world_currency_per_point']),
            'ShowUpFee': int(player.session.config['participation_fee']),
            'CutoffRoll': int(player.session.config['CutoffRoll']),
            'Faction_Number_minus1':  player.session.config['Size'] - 1,

        }


class P02_WaitForGroup(WaitPage):
    template_name = 'DynamicPower_05_Experiment/P02_WaitForGroup.html'
    form_model = 'player'
    form_fields = ['calculatorHistory2']
    @staticmethod
    def after_all_players_arrive(group: Group):
        seq_id = group.session.config['Sequence'] - 1
        if group.session.config['CutoffRoll'] == 10:
            crit_rounds = Constants.cumul10[seq_id]
        crit_rounds[0] = 0
        get_role(group)


        if (group.round_number - 1) in crit_rounds:
            group.roundNumber = 1
            group.matchNumber = int(np.argwhere(crit_rounds == group.round_number - 1)[0][0] + 1)
            
            group.round_line = ", ,"+str(group.roundNumber)+", , "
            group.title_line ="Current Shares, Choice, Earn, Spend, Payoff"
            for p in group.get_players():
                init_match(p)
        else:
            group.matchNumber = group.in_round(group.round_number - 1).matchNumber
            group.roundNumber = int(group.round_number - crit_rounds[group.matchNumber - 1])
            group.round_line = group.in_round(group.round_number - 1).round_line
            group.round_line += ", ,"+str(group.roundNumber)+", , "
            group.title_line  = "Shares, Choice, Earn, Spend, Payoff," + group.in_round(group.round_number - 1).title_line
            
            for p in group.get_players():
                init_round(p)
        
        update_table_content(group)

    @staticmethod
    def vars_for_template(player: Player):
        temp = vars_for_template1(player)
        seq_id = player.session.config['Sequence'] - 1
        if player.session.config['CutoffRoll'] == 10:
            crit_rounds = Constants.cumul10[seq_id]
        crit_rounds[0] = 0

        if (player.round_number - 1) in crit_rounds:
            matchNumber = int(np.argwhere(crit_rounds == player.round_number - 1)[0][0] + 1)
            temp['matchNumber'] = matchNumber
        else:
            temp['matchNumber'] = player.group.matchNumber+1
        return temp
        # if (player.round_number ) in crit_rounds:
            # matchNumber = int(np.argwhere(crit_rounds == player.round_number)[0][0] + 1)
            # temp['matchNumber'] = matchNumber
        # else:
            # temp['matchNumber'] = player.group.matchNumber
        # return temp
    
    is_displayed = is_displayed1
    
     
    @staticmethod
    def js_vars(player):
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


                Exo = player.session.config['Contest'] == 'exogenous',
                
                N = player.session.config['Size'],
                x0 = player.session.config['Half_Effort_normalized'],
                kappa = player.session.config['kappa'] ,
                c = player.session.config['Cost'] ,
                r_0 = player.session.config['R0'] , 
                b =  player.session.config['Benefit'] ,
                fixed_ratio = player.session.config['Ratio'],
               

            )
                   



# This page shows the public contribution & parameters
class P03_Contribution(Page):
    template_name = 'DynamicPower_05_Experiment/P03_Contribution.html'

    form_model = 'player'
    form_fields = []
    
    def get_form_fields(player: Player):
        if player.session.config['Faction_Size'] == 2 and player.id_in_group > player.session.config['Size'] : 
            return ['calculatorHistory3']
        else:
            return ['myChoice', 'calculatorHistory3']
    
    
    
    @staticmethod
    def live_method(player, data):
        print(data)
        if player.session.config['Faction_Size'] == 2  and player.id_in_group <= player.session.config['Size'] : 
            ID_SendTo = player.id_in_group + player.session.config['Size']
            return {ID_SendTo: {"state": "Contributed", "group_choice": player.myChoice}}


    is_displayed = is_displayed1
        
        
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.session.config['Faction_Size'] == 2  and player.id_in_group > player.session.config['Size'] : 
            decider_number = player.id_in_group % player.session.config['Size'] 
            if decider_number== 0 :
                player.myChoice = player.group.get_player_by_id(player.session.config['Size']).myChoice
            else :
                player.myChoice = player.group.get_player_by_id(decider_number).myChoice
        
        player.lineHistory += ","+str( player.myChoice )
   
    vars_for_template = vars_for_template1

    js_vars = js_vars1
    


# This page is to wait for everyone to finish the contribution and belief elicitation;
class P07_WaitForChoice(WaitPage):
    template_name = 'DynamicPower_05_Experiment/P07_WaitForChoice.html'

    form_model = 'player'
    form_fields = ['calculatorHistory7']
    @staticmethod
    def after_all_players_arrive(group: Group):
        get_belief_outcomes(group) 
        get_contribution_outcomes(group)
        
        
       

    is_displayed = is_displayed1
    
    vars_for_template = vars_for_template1
    
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )
    


# This page is for subjects to compete
class P08_Compete(Page):
    template_name = 'DynamicPower_05_Experiment/P08_Compete.html'

    form_model = 'player'
    form_fields = []
    
    def get_form_fields(player: Player):
        if player.session.config['Faction_Size'] == 2 and player.id_in_group > player.session.config['Size'] : 
            return ['calculatorHistory']
        elif player.session.config['Contest'] == "exogenous":
            return ['calculatorHistory8']
        else:
            return ['myEffort', 'calculatorHistory8']
    
    @staticmethod
    def live_method(player, data):
        if player.session.config['Faction_Size'] == 2  and player.id_in_group <= player.session.config['Size'] : 

            ID_SendTo = player.id_in_group + player.session.config['Size']
            return {ID_SendTo: "Competed"}
            
            
    is_displayed = is_displayed1
    
    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if player.session.config['Contest'] == "exogenous":
            player.myEffort = round(float(player.myPayoff) * player.session.config['Ratio'])
            if player.session.config['Faction_Size'] == 2  and player.id_in_group > player.session.config['Size'] : 
                decider_number = player.id_in_group % player.session.config['Size'] 
                if decider_number== 0 :
                    player.myEffort = player.group.get_player_by_id(player.session.config['Size']).myEffort
                else :
                    player.myEffort = player.group.get_player_by_id(decider_number).myEffort
            

        player.lineHistory += "," + str("%.2f" % round(player.myEffort,0)) 
        
    def vars_for_template(player: Player):
        temp =  vars_for_template1(player)
        temp['myEffort_exo'] =  round(float(player.myPayoff) * player.session.config['Ratio'])
        temp['effort_label'] = 'Please decide how much of your {} do you want to put in the power revision?'.format(player.myPayoff)
        return temp
        
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )


class P09_WaitForEffort(WaitPage):
    template_name = 'DynamicPower_05_Experiment/P09_WaitForEffort.html'
    form_model = 'player'
    form_fields = ['calculatorHistory9']
    @staticmethod
    def after_all_players_arrive(group: Group):
        get_competition_outcomes(group)

    is_displayed = is_displayed1



    def vars_for_template(player: Player):
        temp =  vars_for_template1(player)
        temp['myEffort_exo'] =  round(float(player.myPayoff) * player.session.config['Ratio'])
        
        return temp
        
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )




class P10_postMatch(Page):
    template_name = 'DynamicPower_05_Experiment/P10_postMatch.html'


    def is_displayed(player: Player):
        seq_id = player.session.config['Sequence'] - 1

        if player.session.config['CutoffRoll'] == 10:
            crit_rounds = Constants.cumul10[seq_id]
        return (player.round_number) in crit_rounds


    def vars_for_template(player: Player):
        temp =  vars_for_template1(player)
        temp['myEffort_exo'] =  round(float(player.myPayoff) * player.session.config['Ratio'])
        temp['MatchPayoff'] = player.matchPayoff
        return temp
        
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )

    @staticmethod
    def app_after_this_page(player, upcoming_apps):
        seq_id = player.session.config['Sequence'] - 1
        if player.session.config['CutoffRoll'] == 10:
            total_rounds = np.sum(Constants.seqs10[seq_id][0:player.session.config['Matches']])

        if player.round_number == total_rounds:
            return upcoming_apps[0]

    
    

# Here add a page for beleif elicitation
class P04_Belief(Page):
    template_name = 'DynamicPower_05_Experiment/P04_Belief.html'

    form_model = 'player'
    form_fields = []
    @staticmethod
    def get_form_fields(player: Player):
        if player.session.config['Size'] >2: 
            return ['myBelief_firstX',
                    'myBelief_secondX', 
                    'myBelief_thirdX',
                    'calculatorHistory4']
        else:
            return ['myBelief_firstX', 'calculatorHistory4']
        
        
    is_displayed = is_displayed2
    vars_for_template = vars_for_template1
    
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )

# Here add a page for personal norm elicitation
class P05_PersonalNorm(Page):
    template_name = 'DynamicPower_05_Experiment/P05_PersonalNorm.html'


    form_model = 'player'
    form_fields = ['myPNorm_X', 'myPNorm_Y', 'calculatorHistory5']
       
    
    is_displayed = is_displayed2

    vars_for_template = vars_for_template1
    
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )
                    
    

# Here add a page for personal norm elicitation
class P06_SocialNorm(Page):
    template_name = 'DynamicPower_05_Experiment/P06_SocialNorm.html'


    form_model = 'player'
    form_fields = ['mySNorm_X', 'mySNorm_Y', 'calculatorHistory6']
       
    
    is_displayed = is_displayed2

    vars_for_template = vars_for_template1
    
    def js_vars(player):
        d =  js_vars1(player)
        return dict(d, 
                    Choice = player.myChoice,
                    )
                    


# Add one more page for wait until everyone finish competing
# Show the new power
page_sequence = [

    P00_WaitForOthers,
    # Current design: first and last match, belief and personal norm elicitation
    P01_beginExperiment,
    P02_WaitForGroup,
    P03_Contribution,
    P04_Belief,
    P05_PersonalNorm,
    P06_SocialNorm,
    P07_WaitForChoice,
    P08_Compete,
    P09_WaitForEffort,
    P10_postMatch,
    

    
]
