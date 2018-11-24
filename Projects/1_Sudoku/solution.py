
from utils import *


row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units

# TODO: Update the unit list to add the new diagonal units
diag_units=[[r+c for r,c in zip(rows,cols)]]
rev_diag_units= [[r+c for r,c in zip(rows, cols[-1::-1])]]
unitlist = unitlist + diag_units + rev_diag_units


# Must be called after all units (including diagonals) are added to the unitlist
units = extract_units(unitlist, boxes)
peers = extract_peers(units, boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    The naked twins strategy says that if you have two or more unallocated boxes
    in a unit and there are only two digits that can go in those two boxes, then
    those two digits can be eliminated from the possible assignments of all other
    boxes in the same unit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).

    See Also
    --------
    Pseudocode for this algorithm on github:
    https://github.com/udacity/artificial-intelligence/blob/master/Projects/1_Sudoku/pseudocode.md
    """
    # TODO: Implement this function!
    out= values.copy()
    for boxA,valueA in values.items():
        for boxB in peers[boxA]:
            valueB= values[boxB]
            if (len(valueA) == 2) and (len(valueB) == 2) and (valueA == valueB):
                for peer in peers[boxA]&peers[boxB]:
                    for digit in valueA:
                        out[peer]= out[peer].replace(digit,'')
    return out
                
            

def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    # for each box in the puzzle
    for box,value in values.items():
        if len(value)==1:
            # for each peer of the current box
            for peer in peers[box]:
                # check whether the peer has the value
                # if so, remove it
                if len(values[peer])>1:
                    values[peer]= values[peer].replace(value,"")
    return values
            

def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    # for each unit
    for unit in unitlist:
        # for each digit
        for digit in "123456789":
            appear_ct= 0
            appear_box=''
            # check the digit in each box of the unit
            for box in unit:
                # if digit in the box, update counter 
                # and box index
                if digit in values[box]:
                    appear_ct= appear_ct + 1
                    appear_box= box
                # if not unique skip checking
                if appear_ct > 1:
                    break
            # after checking, if unique, update the box
            if appear_ct == 1:
                values[appear_box]= digit
                           
    return values
    

def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    stalled = False
    ct= 1
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Your code here: Use the Eliminate Strategy
        values= eliminate(values)

        # Your code here: Use the Only Choice Strategy
        values= only_choice(values)
        
        # Use the naked twin strategy
        values= naked_twins(values)
                
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
        ct= ct+1
    return values

def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    # termination condifion
    solved_values= len([box for box in values.keys() if len(values[box]) == 1])
    if solved_values==81:
        return values
    
    
    # First, reduce the puzzle using the previous function
    reduced_values= reduce_puzzle(values) 
    if reduced_values== False:
        return False
        
    # Choose one of the unfilled squares with the fewest possibilities
    k_fewest= 'A1'
    min_possibility= 1000 # a big number
    for k,v in reduced_values.items():
        # only for unsolved box
        possibility= len(v) 
        if ( possibility>1) and (possibility< min_possibility):
            min_possibility= possibility
            k_fewest= k
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    # update reduced values
    for v in reduced_values[k_fewest]:
        new_values= reduced_values.copy()
        new_values[k_fewest]= v # replace with one of the possibilities
        attempt= search(new_values)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(grid2values(diag_sudoku_grid))
    result = solve(diag_sudoku_grid)
    display(result)
    

    try:
        import PySudoku
        PySudoku.play(grid2values(diag_sudoku_grid), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
