import cProfile

from Connect4 import Connect4Game
import minimax
#board = Connect4Game(width=5, height=4, in_a_row =4)
cProfile.run('minimax_with_file(Connect4Game(width=4, height=4, in_a_row =4), 16)')