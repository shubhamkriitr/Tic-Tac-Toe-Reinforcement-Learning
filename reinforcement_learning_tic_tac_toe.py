#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 17:29:51 2018

@author: shubham
"""
import numpy as np

class Agent:
    def __init__(self,values,env,alpha=0.2,symbol="X"):
        self.values = np.copy(values.astype(np.float32))  #Value function (Table)
        self.env = env  # Game environment
        self.alpha  = alpha
        self.game_cache = np.zeros(shape=(5,),dtype=np.int16)# at most 5 moves
        #  caN be made (game cache stores index of moves)
        self.explore_prob = 0.1 #  10% random
        self.moves_count = 0
        self.symbol = symbol
        if self.symbol == "X":
            self.num = 2
            self.win_id = 2
            self.lose_id = 0
        elif self.symbol == "O":
            self.num = 0
            self.win_id = 0
            self.lose_id = 2

    def _select_best_move(self,state):
        i = 0
        best_i = None
        best_val = None
        so = None#temp var to hold orignal state
        best_code = None # hash value for state after best move
        if np.random.uniform() < self.explore_prob:
            best_i = self._select_random_move(state)
            so = state[best_i]
            state[best_i] = self.num
            best_code = self.env.state_to_code(state)
            state[best_i] = so
            return (best_i, best_code)
        else:
            for j in range(len(state)):
                if state[i] == 1:
                    best_i = i
                    so = state[i]
                    state[best_i] = self.num
                    best_code = self.env.state_to_code(state)
                    best_val = self.values[best_code]
                    state[best_i] = so
                    break
                i += 1

            i +=1
            while i<9:
                if state[i] == 1:
                    so = state[i]
                    state[i] = self.num
                    code = self.env.state_to_code(state)
                    val = self.values[code]
                    state[i] = so
                    if val > best_val:
                        best_val = val
                        best_i = i
                        best_code = code
                i+=1
            return (best_i, best_code)

    def _select_random_move(self, state):
        idx = np.linspace(0,8,9,dtype=np.int16)
        np.random.shuffle(idx)
        for i in range(9):
            if state[idx[i]] == 1:
                return idx[i]

    def make_move(self):
        """Makes move, updates value function, and returns current conclusion
        of the move made."""
        i, code = self._select_best_move(self.env.get_state())
        self.game_cache[self.moves_count] = code
        self.moves_count+=1
        result = self.env.make_move(i,self.symbol)
        print("Agent ({}):".format(self.symbol),self.env.get_state(), "Result Code:",result)
        if result == 1: # go on
            return "Go"
        elif result == self.win_id: # Won
            self.values[self.game_cache[self.moves_count-1]] = 1.0#win prob
            self.update_table()
            return "Won"
        elif result == self.lose_id:
            self.values[self.game_cache[self.moves_count-1]] = 0.0
            self.update_table()
            return "Lost"
        elif result == -2:
            return "Draw"
        else:
            raise AssertionError("Unexpected Result=".format(result))


    def update_table(self):
        """Assumes value c/t the move for last state has been updated"""
        self.moves_count-=2
        while self.moves_count>=0:
            self.values[self.game_cache[self.moves_count]] += self.alpha*(
                    self.values[self.game_cache[self.moves_count+1]] -
                    self.values[self.game_cache[self.moves_count]])
            self.moves_count-=1
        self.reset_game_cache()

    def reset_game_cache(self):
        self.moves_count = 0

class Opponent:
    def __init__(self,env):
        self.env = env  # Game environment

    def _select_random_move(self, state):
        idx = np.linspace(0,8,9,dtype=np.int16)
        np.random.shuffle(idx)
        for i in range(9):
            if state[idx[i]] == 1:
                return idx[i]

    def make_move(self):
        """Makes move, updates value function, and returns `Over` for game over\
        and `Go` otherwise."""
        i = self._select_random_move(self.env.get_state())
        result = self.env.make_move(i,"O")
        print("Opponent(O):",self.env.get_state(),"Result Code:",result)
        if result == 1: # go on
            return "Go"
        elif result == 2: # opppnent loses
            return "Won"
        elif result == 0:
            return "Lost"
        elif result == -2:
            return "Draw"
        else:
            raise AssertionError("Unexpected Result=".format(result))


class Environment:
    def __init__(self):
        self.state = None  # location of X, O , blanks
        self.state_code = None# 0 to 19682
        self.state_map = np.zeros(shape = (19683,),dtype=np.float32)#  Array of 19683 elements
        self.moves_count = 0
        self.initialize_state_map()
        self.reset_state()

    def initialize_state_map(self):
        self._init_state_map(9,[0,0,0,0,0,0,0,0,0])
        print("State_map",self.state_map,self.state_map.shape)

    def _init_state_map(self,remaining,state):
        if remaining == 0:
            s_code = self.state_to_code(state)
            prob = self._status_check(state)
            print(s_code,"=",state,"=",prob)
            self.state_map[s_code] = prob
        else:
            for i in range(3):
                state[remaining-1] = i
                self._init_state_map(remaining - 1, state)



    def state_to_code (self,state):
        code = 0
        for i in range(8):
            code = 3*(code + state[8-i])
        code += state[0]
        return code


    def _status_check(self,state):
        """returns -1 0 1 or 0.5 for invalid, lose, win,
        valid(but not win/lose) states"""
        wins = {"0":0,"2":0}# 0 == O  2 == X

        #vertical
        for i in [8,7,6]:
            sm = 0
            for j in range(3):
                sm+=state[i-3*j]# 8-5-2 7-4-1 ..
            if sm == 6:
                wins["2"] += 1
            elif sm == 0:
                wins["0"] += 1

        #horizontal
        for i in[8,5,2]:
            sm = 0
            for j in range(3):
                sm += state[i-j]#8-7-6 5-4-3 ..
            if sm == 6:
                wins["2"] += 1
            elif sm == 0:
                wins["0"] += 1

        #diagonal
        for d in [[8,4,0],[6,4,2]]:
            sm = 0
            for j in d:
                sm += state[j]#8-7-6 5-4-3 ..
            if sm == 6:
                wins["2"] += 1
            elif sm == 0:
                wins["0"] += 1

        if (wins["2"] + wins["0"])>1:
            return -1 # invalid state

        if wins["2"] == 1:
            return 1

        if wins["0"] == 1:
            return 0

        return 0.5 # other valid state

    def reset_state(self):
        self.state = [1,1,1,1,1,1,1,1,1]  # All blanks
        self.state_code = self.state_to_code(self.state)
        self.moves_count = 0
        #  i.e <a8,a7,a5,a4,a3,a2,a1,a0>
        #  ai = 0,1 & 2 corresponds to O, blank, & X resp.
        #  a8 a7 a6// base-3 representation of game-matrix
        #  a5 a4 a3
        #  a2 a1 a0

    def get_state(self):
        return self.state

    def make_move(self,index,value):
        if value == "O":
            self.state[index] = 0
        elif value == "X":
            self.state[index] = 2
        self.moves_count += 1
        self.state_code = self.state_to_code(self.state)
        return self.check_status()

    def set_state(self,state):
        self.state = state

    def check_status(self):
        """Returns:
            game_state(`int`):-2 -1 0 1 or 2
                               -2 = Draw
                               -1 = Invalid State
                               0 = O won/ X lost
                               1 = Game still on
                               2 = X won
        """
        if self.moves_count < 5:
            return 1
        elif self.moves_count == 9:
            return -2
        else:
            return self._check_status()

    def _check_status(self):
        #print("stat check:",self.state_map[self.state_code])
        if self.state_map[self.state_code] == 1:
            return 2
        elif self.state_map[self.state_code] == 0:
            return 0
        elif self.state_map[self.state_code] == -1:
            return -1
        else:
            return 1

if __name__ == "__main__":
    env = Environment()
    print(env.state_to_code([1,0,0,0,0,0,0,0,2]))
    print(2*pow(3,8)+1)
    env._init_state_map(9,[0,0,0,0,0,0,0,0,0])
    print(env.state_map)
    print(env.state_map.shape)
    env.initialize_state_map()
