# -*- coding: utf-8 -*-
import unittest
from utils import *
import solution as sln

class TestSudoku(unittest.TestCase):
    def setUp(self):
        row_units = [cross(r, cols) for r in rows]
        column_units = [cross(rows, c) for c in cols]
        square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
        unitlist = row_units + column_units + square_units
        
        # TODO: Update the unit list to add the new diagonal units
        diag_units= [r+c for r,c in zip(rows,cols)]
        rev_diag_units= [r+c for r,c in zip(rows, cols[-1::-1])]
        unitlist = unitlist + diag_units + rev_diag_units
        
        
        # Must be called after all units (including diagonals) are added to the unitlist
        self.units = extract_units(unitlist, boxes)
        self.peers = extract_peers(units, boxes)
        
        self.grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
        self.values= sln.grid2values(self.grid)
        print("Original Puzzle:")
        display(self.values)
    
    def test_eliminate(self):
        values= sln.eliminate(self.values)
        print("Puzzle after eliminate:")
        display(values)
        self.assertEqual(isinstance(values,dict), True)
    
    def test_only_choice(self):
        values_elim= sln.eliminate(self.values)
        values= sln.only_choice(values_elim)
        print ("Puzzle after eliminate and only_choice:")
        display(values)
        self.assertEqual(isinstance(values,dict), True)
        
    def test_naked_twin(self):
        values_elim= sln.eliminate(self.values)
        values_only= sln.only_choice(values_elim)
        values= sln.naked_twins(values_only)
        print ("Puzzle after eliminate and only_choice and naked_twin:")
        display(values)
        self.assertEqual(isinstance(values,dict), True)
        
        
if __name__=='__main__':
    unittest.main()
        
    

        
