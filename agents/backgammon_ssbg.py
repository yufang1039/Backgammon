'''
Name(s): Alex Lin, Yu Fang
UW netid(s): alexlin2 yfang35
'''

from game_engine import genmoves
import random

MIN, MAX = -1000, 1000

class BackgammonPlayer:
    def __init__(self):
        self.GenMoveInstance = genmoves.GenMoves()
        self.move_generator = None
        self.statesExpanded = 0
        self.staticEvalFunc = self.staticEval
        self.maxPly = 2
        self.currentState = None

    # returns a string representing a unique nick name for your agent
    def nickname(self):
        # TODO: return a string representation of your UW netid(s)
        return "AlexFang"

    # Returns a tuple containing the number explored
    # states as well as the number of cutoffs.
    def statesAndCutoffsCounts(self):
        return (self.statesExpanded, self.AlphaBetaCutoffs)

    # Given a ply, it sets a maximum for how far an agent
    # should go down in the search tree. If maxply==-1,
    # no limit is set
    def setMaxPly(self, maxply=-1):
        self.maxPly = maxply

    # If not None, it update the internal static evaluation
    # function to be func
    def useSpecialStaticEval(self, func):
        if func: self.staticEvalFunc = func
        else: self.staticEvalFunc = self.staticEval

    # Given a state and a roll of dice, it returns the best move for
    # the state.whose_move
    def move(self, state, die1, die2):
        # TODO: return a move for the current state and for the current player.
        # Hint: you can get the current player with state.whose_move
        self.currentState = state
        maximizingPlayer = state.whose_move == 0
        self.move_generator = self.GenMoveInstance.gen_moves(state, state.whose_move, die1, die2)
        move_list, state_list = self.get_all_possible_moves()
        self.statesExpanded += len(move_list)
        bestMove = None
        depth = 0
        bestScore = MIN if maximizingPlayer else MAX

        for i in range(len(move_list)):
            if maximizingPlayer:
                val = self.expectiminimax(depth+1, state_list[i], 2, 1, die1, die2)
                if val > bestScore:
                    bestScore = val
                    bestMove = move_list[i]
            else:
                val = self.expectiminimax(depth+1, state_list[i], 2, 0, die1, die2)
                if val < bestScore:
                    bestScore = val
                    bestMove = move_list[i]

        return bestMove

    def expectiminimax(self, depth, state, whichPlayer, nextChange, die1, die2):
        if depth == self.maxPly or len(state.red_off) == 15 or len(state.white_off) == 15:
            return self.staticEvalFunc(state)
        
        if whichPlayer == 0 or whichPlayer == 1:
            who = 0 if whichPlayer == 0 else 1
            self.move_generator = self.GenMoveInstance.gen_moves(state, who, die1, die2)
            move_list, state_list = self.get_all_possible_moves()
        
        self.statesExpanded += 1

        if whichPlayer == 0:
            best = MIN
            for nextState in state_list:
                val = self.expectiminimax(depth+1, nextState, 2, 1, die1, die2)
                best = max(best, val)  
            return best
        
        elif whichPlayer == 1:
            best = MAX
            for nextState in state_list:
                val = self.expectiminimax(depth+1, nextState, 2, 0, die1, die2)
                best = min(best, val)  
            return best

        else:
            for i in range(1, 7):
                for j in range(1, i + 1):
                    best = 0
                    val = self.expectiminimax(depth, state, nextChange, nextChange, i, j)
                    best += val / 21
            return best


    def useUniformDistribution():
        pass

    # Given a state, returns an integer which represents how good the state is
    # for the two players (W and R) -- more positive numbers are good for W
    # while more negative numbers are good for R
    def staticEval(self, state):
        score = 0
        score += state.pointLists[0].count(0) * -10
        score += state.pointLists[1].count(0) * -10
        score += state.pointLists[2].count(0) * -10
        score += state.pointLists[3].count(0) * -10
        score += state.pointLists[4].count(0) * -10
        score += state.pointLists[5].count(0) * -10
        score += state.pointLists[6].count(0) * 2
        score += state.pointLists[7].count(0) * 2
        score += state.pointLists[8].count(0) * 2
        score += state.pointLists[9].count(0) * 2
        score += state.pointLists[10].count(0) * 2
        score += state.pointLists[11].count(0) * 2
        score += state.pointLists[12].count(0) * 5
        score += state.pointLists[13].count(0) * 5
        score += state.pointLists[14].count(0) * 5
        score += state.pointLists[15].count(0) * 5
        score += state.pointLists[16].count(0) * 5
        score += state.pointLists[17].count(0) * 5
        score += state.pointLists[18].count(0) * 100
        score += state.pointLists[19].count(0) * 10
        score += state.pointLists[20].count(0) * 10
        score += state.pointLists[21].count(0) * 10
        score += state.pointLists[22].count(0) * 10
        score += state.pointLists[23].count(0) * 100

        score += len(state.white_off) * 1000
        score += state.bar.count(0) * -500

        score -= state.pointLists[0].count(1) * 100
        score -= state.pointLists[1].count(1) * 10
        score -= state.pointLists[2].count(1) * 10
        score -= state.pointLists[3].count(1) * 10
        score -= state.pointLists[4].count(1) * 10
        score -= state.pointLists[5].count(1) * 100
        score -= state.pointLists[6].count(1) * 5
        score -= state.pointLists[7].count(1) * 5
        score -= state.pointLists[8].count(1) * 5
        score -= state.pointLists[9].count(1) * 5
        score -= state.pointLists[10].count(1) * 5
        score -= state.pointLists[11].count(1) * 5
        score -= state.pointLists[12].count(1) * 2
        score -= state.pointLists[13].count(1) * 2
        score -= state.pointLists[14].count(1) * 2
        score -= state.pointLists[15].count(1) * 2
        score -= state.pointLists[16].count(1) * 2
        score -= state.pointLists[17].count(1) * 2
        score -= state.pointLists[18].count(1) * -10
        score -= state.pointLists[19].count(1) * -10
        score -= state.pointLists[20].count(1) * -10
        score -= state.pointLists[21].count(1) * -10
        score -= state.pointLists[22].count(1) * -10
        score -= state.pointLists[23].count(1) * -10

        score += state.bar.count(1) * 500
        score += len(state.red_off) * -1000

        return score


    def get_all_possible_moves(self):
        """Uses the mover to generate all legal moves. Returns an array of move commands"""
        move_list = []
        state_list = []
        done_finding_moves = False
        any_non_pass_moves = False
        while not done_finding_moves:
            try:
                m = next(self.move_generator)    # Gets a (move, state) pair.
                # print("next returns: ",m[0]) # Prints out the move.    For debugging.
                if m[0] != 'p':
                    any_non_pass_moves = True
                    move_list.append(m[0])    # Add the move to the list.
                    state_list.append(m[1])
            except StopIteration as e:
                done_finding_moves = True
        if not any_non_pass_moves:
            move_list.append('p')
            state_list.append(self.currentState)
        return move_list, state_list
