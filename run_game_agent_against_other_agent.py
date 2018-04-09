#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 21:15:39 2018

@author: shubham
"""

from reinforcement_learning_tic_tac_toe import Agent, Opponent, Environment
import numpy as np
np.random.seed(0)

env = Environment()

agnt = Agent(env.state_map,env,alpha=0.1,symbol="X")#Agent 1
opnt_agnt = Agent(env.state_map,env,alpha=0.05,symbol="O")# Agent 2

N = 15000 # Number of training games to be played
won_count = 0
lost_count = 0
draw_count = 0

for game_count in range(1,N+1):
    env.reset_state()
    agnt.reset_game_cache()
    opnt_agnt.reset_game_cache()
    print("=======Game({})=========".format(game_count))
    i = 0 # opnt goes furst
    if np.random.uniform() < 0.5:
        i = 1 # Agnt goes first
    while True:
        if i % 2 == 0:
            outcome = opnt_agnt.make_move()
        else:
            outcome = agnt.make_move()
        if outcome == "Won":
            if i%2 == 0:
                lost_count += 1#agent 2 or opnt won
            else:
                won_count+=1
            break
        elif outcome == "Lost":
            if i%2 == 0:
                won_count += 1 #agent 2 lost
            else:
                lost_count+=1
            break
        elif outcome == "Draw":
            draw_count += 1
            break
        i+=1
    print("Games Played:",game_count,"Won:",won_count,"Lost:",lost_count,
          "Draw:", draw_count)

dummy = input("Press Enter to test trained Agent(X) against imperfect player:")

opnt = Opponent(env)
N = 1000 # Number of training games to be played
won_count = 0
lost_count = 0
draw_count = 0

for game_count in range(1,N+1):
    env.reset_state()
    agnt.reset_game_cache()
    print("=======Game({})=========".format(game_count))
    i = 0 # opnt goes furst
    if np.random.uniform() < 0.5:
        i = 1 # Agnt goes first
    while True:
        if i % 2 == 0:
            outcome = opnt.make_move()
        else:
            outcome = agnt.make_move()
        if outcome == "Won":
            won_count+=1
            break
        elif outcome == "Lost":
            lost_count+=1
            break
        elif outcome == "Draw":
            draw_count += 1
            break
        i+=1
    print("Games Played:",game_count,"Won:",won_count,"Lost:",lost_count,
          "Draw:", draw_count)