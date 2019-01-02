
from sample_players import DataPlayer


class CustomPlayer(DataPlayer):
    """ Implement your own agent to play knight's Isolation

    The get_action() method is the only required method for this project.
    You can modify the interface for get_action by adding named parameters
    with default values, but the function MUST remain compatible with the
    default interface.

    **********************************************************************
    NOTES:
    - The test cases will NOT be run on a machine with GPU access, nor be
      suitable for using any other machine learning techniques.

    - You can pass state forward to your agent on the next turn by assigning
      any pickleable object to the self.context attribute.
    **********************************************************************
    """
    def get_action(self, state):
        """ Employ an adversarial search technique to choose an action
        available in the current state calls self.queue.put(ACTION) at least

        This method must call self.queue.put(ACTION) at least once, and may
        call it as many times as you want; the caller will be responsible
        for cutting off the function after the search time limit has expired.

        See RandomPlayer and GreedyPlayer in sample_players for more examples.

        **********************************************************************
        NOTE: 
        - The caller is responsible for cutting off search, so calling
          get_action() from your own code will create an infinite loop!
          Refer to (and use!) the Isolation.play() function to run games.
        **********************************************************************
        """
        # TODO: Replace the example implementation below with your own search
        #       method by combining techniques from lecture
        #
        # EXAMPLE: choose a random move without any search--this function MUST
        #          call self.queue.put(ACTION) at least once before time expires
        #          (the timer is automatically managed for you)
        
        import random
        #self.queue.put(random.choice(state.actions()))
        
       
        
        depth_limit= 4
        if state.ply_count < 2:
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax_decision(state, depth_limit))
            #self.queue.put(self.minimax(state,depth_limit))
        
    def score_default(self,gameState):
        # TODO: Finish this function!
        # HINT: the global player_id variable is accessible inside
        #       this function scope
        #global player_id
        own_loc = gameState.locs[self.player_id]
        opp_loc = gameState.locs[1 - self.player_id]
        own_liberties = gameState.liberties(own_loc)
        opp_liberties = gameState.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)

    # TODO: modify the function signature to accept an alpha and beta parameter
    def min_value(self, gameState, alpha, beta, depth=1):
        """ Return the value for a win (+1) if the game is over,
        otherwise return the minimum value over all legal child
        nodes.
        """
        if gameState.terminal_test():
            return gameState.utility(self.player_id)
        
        # New conditional depth limit cutoff
        if depth <= 0:  # "==" could be used, but "<=" is safer 
            return self.score_default(gameState)
        
        v = float("inf")
        for a in gameState.actions():
            # TODO: modify the call to max_value()
            v = min(v, self.max_value(gameState.result(a),alpha,beta,depth-1))
            # TODO: update the value bound
            if v<= alpha: return v
            beta= min(v, beta)
        return v
    
    # TODO: modify the function signature to accept an alpha and beta parameter
    def max_value(self, gameState, alpha, beta, depth= 1):
        """ Return the value for a loss (-1) if the game is over,
        otherwise return the maximum value over all legal child
        nodes.
        """
        if gameState.terminal_test():
            return gameState.utility(self.player_id)
        
        # New conditional depth limit cutoff
        if depth <= 0:  # "==" could be used, but "<=" is safer 
            return self.score_default(gameState)
            
        v = float("-inf")
        for a in gameState.actions():
            # TODO: modify the call to min_value()
            v = max(v, self.min_value(gameState.result(a), alpha, beta, depth-1))
            # TODO: update the value bound
            if v>=beta: return v
            alpha= max(v,alpha)
        return v

    def minimax_decision(self,gameState, depth):
        """ Return the move along a branch of the game tree that
        has the best possible value.  A move is a pair of coordinates
        in (column, row) order corresponding to a legal move for
        the searching player.
        
        You can ignore the special case of calling this function
        from a terminal state.
        """
        
        alpha= float("-inf")
        beta= float("inf")
        
        best_score = float("-inf")
        best_move = None
        for a in gameState.actions():
            # call has been updated with a depth limit
            v = self.min_value(gameState.result(a), alpha, beta, depth-1)
            #alpha= max(v,alpha)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move
        
        #return max(gameState.actions(), \
        #           key=lambda x: self.min_value(gameState.result(x),alpha, beta, depth - 1))

    
    def minimax(self, state, depth):

        def min_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score_default(state)
            value = float("inf")
            for action in state.actions():
                value = min(value, max_value(state.result(action), depth - 1))
            return value

        def max_value(state, depth):
            if state.terminal_test(): return state.utility(self.player_id)
            if depth <= 0: return self.score_default(state)
            value = float("-inf")
            for action in state.actions():
                value = max(value, min_value(state.result(action), depth - 1))
            return value

        return max(state.actions(), key=lambda x: min_value(state.result(x), depth - 1))
