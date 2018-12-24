# -*- coding: utf-8 -*-

import minimax_helpers

from gamestate import *

g = GameState()
inf = float("inf")
actions = [((0, 0), inf), ((1, 0), -inf), ((2, 0), inf), ((0, 1), inf), ((1, 1), -inf)]

if all(minimax_helpers.min_value(g.result(a)) == ev for a, ev in actions):
    print("Looks like everything works!")
else:
    print("Uh oh! Not all the scores matched.")

