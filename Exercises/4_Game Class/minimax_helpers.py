# -*- coding: utf-8 -*-


#%% helper functions
def min_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the minimum value over all legal successors
    
    # HINT: Assume that the utility is ALWAYS calculated for
            player 1, NOT for the "active" player
    """
    # TODO: finish this function!
    if type(gameState)=='float':
        haha= 1
    
    if gameState.terminal_test():
        return gameState.utility(0)
    v= float("inf")
    for a in gameState.actions():
        v= min(v, max_value(gameState.result(a)))
    return v


def max_value(gameState):
    """ Return the game state utility if the game is over,
    otherwise return the maximum value over all legal successors
    
    # HINT: Assume that the utility is ALWAYS calculated for
            player 1, NOT for the "active" player
    """
    # TODO: finish this function!
    if type(gameState)=='float':
        haha= 1
    if gameState.terminal_test():
        return gameState.utility(0)
    v= float("-inf")
    for a in gameState.actions():
        v= max(v,min_value(gameState.result(a)))
    return v

