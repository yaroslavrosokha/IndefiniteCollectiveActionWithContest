from otree.api import Currency as c, currency_range
from . import *
from otree.api import Bot
import random



class PlayerBot(Bot):

    def play_round(self):
        
        # seqs10 = [
            # [11, 6, 1, 2, 9, 1, 20, 6, 7, 16],
            # [1, 1, 14, 1, 17, 6, 4, 1, 7, 8],
            # [7, 9, 17, 4, 18, 10, 13, 2, 3, 3],
            # [4, 2, 3, 2, 9, 11, 3, 4, 2, 19, 11, 35, 2, 5, 8, 5, 2, 10, 27, 6],
            # [2, 5, 13, 4, 9, 4, 3, 12, 8, 16]]

        seqs10 = [
            [4, 2, 3, 2, 9, 11, 3, 4, 2, 19, 11, 35, 2, 5, 8, 5, 2, 10, 27, 6],
            [9, 6, 21, 5, 3, 7, 12, 5, 5, 12, 18, 7, 7, 17, 5, 2, 48, 4, 2, 9],
            [16, 4, 9, 11, 18, 21, 2, 3, 14, 2, 6, 22, 13, 9, 3, 9, 7, 6, 18, 17],
            [2, 7, 36, 41, 2, 5, 7, 12, 3, 18, 2, 21, 2, 1, 1, 5, 6, 2, 9, 1], 
            [9, 10, 21, 16, 4, 3, 9, 40, 3, 35, 11, 46, 4, 17, 1, 31, 3, 4, 4, 1], 
            ]
        cumul10 = [np.roll(np.cumsum(s, dtype=int), 1) for s in seqs10]

        seq_id = self.session.config['Sequence'] - 1
        total_rounds = np.sum(seqs10[seq_id][0:self.session.config['Matches']])
        crit_rounds = cumul10[seq_id]
        
        
        if self.round_number ==1: 
            yield P01_beginExperiment
        
        # display 1
        if self.round_number <= total_rounds :
            
            yield P03_Contribution, dict(myChoice = random.choice([0,1]))
                
            #display 2
            if  self.group.matchNumber ==  1 or self.group.matchNumber ==  self.session.config['Matches'] or self.group.matchNumber ==  10  :
                if self.session.config['Size'] >2: 
                    yield P04_Belief, dict(myBelief_firstX = 80, myBelief_secondX = 100, myBelief_thirdX = 100 )
                else :
                    yield P04_Belief, dict(myBelief_firstX = 20 )
                
                yield P05_PersonalNorm, dict(myPNorm_X=1, myPNorm_Y=1)
                yield P06_SocialNorm,dict(mySNorm_X=1, mySNorm_Y=1)

            if self.session.config['Contest'] == "exogenous" or ( self.session.config['Faction_Size'] == 2 and self.id_in_group > self.session.config['Size'] ):
                yield Submission(P08_Compete, check_html=False)
            else :
                yield Submission(P08_Compete, dict(myEffort = random.randint(0,40)), check_html=False)
            
            if self.round_number in crit_rounds and  self.round_number <= total_rounds:
                yield P10_postMatch
    
