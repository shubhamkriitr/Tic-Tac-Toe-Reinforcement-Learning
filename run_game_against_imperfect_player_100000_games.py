#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  9 21:15:39 2018

@author: shubham
"""

from reinforcement_learning_tic_tac_toe import Agent, Opponent, Environment
import numpy as np
import h5py as hf
np.random.seed(0)

env = Environment()

agnt = Agent(env.state_map,env,alpha=0.5)
opnt = Opponent(env)

N = 100000 # Number of training games to be played
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
print("Saving Weights")
with hf.File('100000_games.h5','w') as f:
    f.create_dataset("value_function",data=agnt.values)