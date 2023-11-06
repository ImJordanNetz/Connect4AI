from Connect4 import Connect4Game
import json

seen_boards = []

def ab_pruning(board, depth, alpha=float("-inf"), beta=float("inf")):
    global seen_boards
    legal_moves = board.generate_legal_moves()
    
    if board.isWin == 1:
        if (board.turn + 1) % 2: #(board.turn + 1) % 2 is how to get to the next player
            return (-1*(depth+1), board.moves[-1])
        else:
            return (1*(depth+1), board.moves[-1])
    
    if len(legal_moves) == 0:
        return (0, board.moves[-1])
    
    
        
    if depth != 0:
        
        if board.turn == 0:
            max_eval = (float('-inf'), 0)
            for move in range(len(legal_moves)):
                
                
                new_board = Connect4Game(board)
                new_board.play_move(legal_moves[move])
                new_board_array = new_board.relevent_board
                board_str = json.dumps(new_board_array)
                board_str_rev = json.dumps(new_board_array[::-1])
                if board_str in seen_boards:
                    eval = (seen_boards[board_str], legal_moves[move])
                elif board_str_rev in seen_boards: 
                    eval = (seen_boards[board_str_rev], legal_moves[move])
                    
                    
                    
                else:
                    eval = ab_pruning(new_board, depth-1, alpha, beta)
                if eval[0] > max_eval[0]:
                    max_eval = (eval[0], legal_moves[move])
                alpha = max(alpha, eval[0])
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = (float('inf'), 0)
            for move in range(len(legal_moves)):
                
                
                new_board = Connect4Game(board)
                new_board.play_move(legal_moves[move])
                new_board_array = new_board.relevent_board
                board_str = json.dumps(new_board_array)
                board_str_rev = json.dumps(new_board_array[::-1])
                if board_str in seen_boards:
                    eval = (seen_boards[board_str], legal_moves[move])
                elif board_str_rev in seen_boards: 
                    eval = (seen_boards[board_str_rev], legal_moves[move])
                    
                    
                    
                else:
                    eval = ab_pruning(new_board, depth-1, alpha, beta)
                
                
                if eval[0] < min_eval[0]:
                    min_eval = (eval[0], legal_moves[move])
                beta = min(beta, eval[0])
                if beta <= alpha:
                    break
            return min_eval
    


def play_game_v_AI(board, player):
    print(board.display_board())
    while board.isWin == 0:
        #0 means human player 1, 1 means AI player 2
        if board.turn == player-1:
            board.play_move(int(input(f"Player {board.turn+1}, it is your move. Type 0 -> {board.width-1}: ")))
        else:
            move = ab_pruning(board, board.width*board.height)
            board.play_move(move[1])
            print("The AI has moved")
            print(f"AI Eval: {move[0]}")
        
            print(board.display_board())
    print(board.display_board())
    if board.isWin == 1:
        print(f"Player {(board.turn+1) % 2 + 1} won!")
    else: print(f"It is a tie!")

import time
start_time = time.time()
board = Connect4Game(width=4, height=5, in_a_row =3)
ab_pruning(board, depth=board.width*board.height)
print ("My program took", time.time() - start_time, "to run")