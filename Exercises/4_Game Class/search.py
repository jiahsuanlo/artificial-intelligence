# -*- coding: utf-8 -*-

from minimax_iterative_deepening import minimax_decision

def get_action(gameState, depth_limit):
    # TODO: Implement a function that calls minimax_decision
    # for each depth from 1...depth_limit (inclusive of both endpoints)
    
    for d in range(1,depth_limit+1):
        best_action= minimax_decision(gameState, d)

    return best_action