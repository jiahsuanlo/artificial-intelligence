# -*- coding: utf-8 -*-
from minimax_helpers import *


def minimax_decision(gameState):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """
    # TODO: Finish this function!
    
    alist= gameState.actions()
    vlist= [min_value(gameState.result(a)) for a in alist]
    valist= [t for t in zip(vlist, alist)]
    vamax= max(valist, key=lambda x:x[0])
    
    return vamax[1]
