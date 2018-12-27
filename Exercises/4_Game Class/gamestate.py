# -*- coding: utf-8 -*-

# TODO: implement the __init__ class below by adding properties
# that meet the three requirements specified
import copy

call_counter = 0
xlim= 3
ylim= 2
class GameState:

    def __init__(self):
        """The GameState class constructor performs required
        initializations when an instance is created. The class
        should:
        
        1) Keep track of which cells are open/closed
        2) Identify which player has initiative
        3) Record the current location of each player
        
        Parameters
        ----------
        self:
            instance methods automatically take "self" as an
            argument in python
        _board: board[x][y], 0:open and 1:closed
        _parity: 0:player1 , 1:player2
        _player_locations: [(x1,y1),(x2,y2)]
        Returns
        -------
        None
        """
        # You can define attributes like this:
        # self.value = 73  # an arbitrary number
        # reassign it to a string (variable type is dynamic in Python)
        # self.value = "some string"
        # self.foo = []  # create an empty list
        self._board=[[0]*ylim for _ in range(xlim)]
        self._board[-1][-1] = 1  # block lower-right corner
        self._parity= 0
        self._player_locations= [None, None]
    
    def liberties(self, loc):
        """ Return a list of all open cells in the
        neighborhood of the specified location.  The list 
        should include all open spaces in a straight line
        along any row, column or diagonal from the current
        position. (Tokens CANNOT move through obstacles
        or blocked squares in queens Isolation.)
        
        Note: if loc is None, then return all empty cells
        on the board
        """
        # if input is none, return all empty cells
        if loc==None:
            open_cells= []
            for x in range(xlim):
                for y in range(ylim):
                    if self._board[x][y]==0:
                        open_cells.append((x,y))
            return open_cells
            
        
        steps= [(1,0),(1,1),(0,1),(-1,1),(-1,0),(-1,-1),(0,-1),(1,-1)]
        open_cells=[]
        for s in steps:
            newloc= loc
            while True:
                newloc= (newloc[0]+ s[0],newloc[1]+s[1])
                if newloc[0] >= 0 and newloc[0]<xlim and\
                newloc[1]>=0 and newloc[1]<ylim and \
                self._board[newloc[0]][newloc[1]]==0:
                    open_cells.append(newloc)
                else:
                    break
        return open_cells
        
    def actions(self):
        """ Return a list of legal actions for the active player 
        
        You are free to choose any convention to represent actions,
        but one option is to represent actions by the (row, column)
        of the endpoint for the token. For example, if your token is
        in (0, 0), and your opponent is in (1, 0) then the legal
        actions could be encoded as (0, 1) and (2,0).
        """
        # TODO: Finish this function!
        return self.liberties(self._player_locations[self._parity])
    
    def player(self):
        """ Return the id of the active player 
        
        Hint: return 0 for the first player, and 1 for the second player
        """
        # TODO: Finish this function!
        return self._parity
    
    def result(self, action):
        """ Return a new state that results from applying the given
        action in the current state
        
        Hint: Check out the deepcopy module--do NOT modify the
        objects internal state in place
        """
        # TODO: Finish this function!
        assert action in self.actions()
        
        new_state= copy.deepcopy(self)
        iplayer= self.player()
        
        new_state._board[action[0]][action[1]]= 1
        new_state._parity^=1
        new_state._player_locations[iplayer]= action
        return new_state
    
    def terminal_test(self):
        """ return True if the current state is terminal,
        and False otherwise
        
        Hint: an Isolation state is terminal if _either_
        player has no remaining liberties (even if the
        player is not active in the current state)
        """
        # TODO: Finish this function!
        global call_counter
        call_counter += 1
        for loc in self._player_locations:
            open_cells= self.liberties(loc)
            if len(open_cells)==0:
                return True
        return False   
    def utility(self, player_id):
        """ return +inf if the game is terminal and the
        specified player wins, return -inf if the game
        is terminal and the specified player loses, and
        return 0 if the game is not terminal
        """
        if not self.terminal_test(): return 0
        player_id_is_active = (player_id == self.player())
        action_list= self.actions()
        active_has_liberties = (len(action_list)>0)
        active_player_wins = (active_has_liberties == player_id_is_active)
        return float("inf") if active_player_wins else float("-inf")


#%% main 
if __name__ == "__main__":
    # This code is only executed if "gameagent.py" is the run
    # as a script (i.e., it is not run if "gameagent.py" is
    # imported as a module)
    emptyState = GameState()  # create an instance of the object
    
    emptyState._board[0][0]= 1
    emptyState._board[2][1]= 1
    print("liberty(1,1):",emptyState.liberties((1,1)))
    
    emptyState._player_locations[0]= (1,1)
    print("current player id:",emptyState.player())
    print("actions:", emptyState.actions())
    newState= emptyState.result((2,0))
    
    newState1= newState.result((1,1))
    print("actions for newState1:", newState1.actions())
    
    newState2= newState1.result((1,0))
    print("actions for newState2:", newState2.actions())
    
    newState3= newState2.result((0,1))
    print("actions for newState3:", newState3.actions())
    
    print("newState terminate:", newState.terminal_test())
    print("newState1 terminate:", newState1.terminal_test())
    print("newState2 terminate:", newState2.terminal_test())
    print("newState3 terminate:", newState3.terminal_test())
    