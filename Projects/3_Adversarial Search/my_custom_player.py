from sample_players import DataPlayer
# board array dimensions and bitboard size
_WIDTH = 11
_HEIGHT = 9
_SIZE = (_WIDTH + 2) * _HEIGHT - 2

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
        
#        self.score= self.score_moves
#        self.score= self.score_center
#        self.score= self.score_moves2
        self.score= self.score_progression
        
        depth_limit= 5
        if state.ply_count < 2:            
            self.queue.put(random.choice(state.actions()))
        else:
            self.queue.put(self.minimax_decision(state, depth_limit))
           
    def score_moves(self,gameState):
        """ Default evaluation function: 
        number of current player liberties - number of opposing player liberties
        """
        own_loc = gameState.locs[self.player_id]
        opp_loc = gameState.locs[1 - self.player_id]
        own_liberties = gameState.liberties(own_loc)
        opp_liberties = gameState.liberties(opp_loc)
        return len(own_liberties) - len(opp_liberties)
    
    def score_moves2(self,gameState):
        """ Extended liberty differences evaluation function
        This evaluation function is defined as the difference in the number of 
        extended liberties between current and opposing players. The extended 
        liberties are defined as the allowable moves for the current location as 
        well as all of next possible locations  
        """
        own_loc = gameState.locs[self.player_id]
        opp_loc = gameState.locs[1 - self.player_id]
        own_liberties = gameState.liberties(own_loc)
        opp_liberties = gameState.liberties(opp_loc)
        
        # Calculate the liberties for each liberty location of the current player
        own_set= set(own_liberties)
        for o in own_liberties:
            own_set.update(gameState.liberties(o))
        # Calculate the liberties for each liberty location of the opposing player
        opp_set= set(opp_liberties)
        for o in opp_liberties:
            opp_set.update(gameState.liberties(o))
        
        return len(own_set) - len(opp_set)
    
    def score_center(self,gameState):
        """ Evaluation function for occupying center location
        This evaluation function rewards the current player to be as close 
        to center location as possible, and rewards the opposing player to
        be as far away from center as possible
        
        """
        own_loc = gameState.locs[self.player_id]
        opp_loc = gameState.locs[1 - self.player_id]
        
        center_loc= _SIZE//2
        own_x= own_loc%(_WIDTH+2)
        own_y= own_loc//(_WIDTH+2)
        opp_x= opp_loc%(_WIDTH+2)
        opp_y= opp_loc//(_WIDTH+2)
        center_x= center_loc%(_WIDTH+2)
        center_y= center_loc//(_WIDTH+2)
        # own player needs to be close to center and opp needs to be far 
        # away from center
        own_center_dist = abs(own_x - center_x) + abs(own_y - center_y) 
        opp_center_dist = abs(opp_x - center_x) + abs(opp_y - center_y)
        return -own_center_dist + opp_center_dist
        
    def score_progression(self, gameState):
        # count the open locations
        n_open_spots= bin(gameState.board).count('1')
        if n_open_spots >80:
            final_score= self.score_center(gameState)
        elif n_open_spots >60:                
            final_score= self.score_moves(gameState)
        else:
            final_score= self.score_moves2(gameState)
        
        return final_score
    
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
            return self.score(gameState)
        
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
            return self.score(gameState)
            
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
        best_move =  gameState.actions()[0]
        for a in gameState.actions():
            # call has been updated with a depth limit
            v = self.min_value(gameState.result(a), alpha, beta, depth-1)
            alpha= max(v,alpha)
            if v > best_score:
                best_score = v
                best_move = a
        return best_move       
        
