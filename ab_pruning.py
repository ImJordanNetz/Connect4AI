from Connect4 import Connect4Game
import json

seen_boards = {}


def set_solved(board):
    global seen_boards
    print('opening file...')
    board_type = f"{board.width}x{board.height}x{board.in_a_row}"
    try:
        with open(f'./solved/{board_type}.json', 'r') as f:
            try:
                print('loading file...')
                loaded_data = json.load(f)
                seen_boards = loaded_data
                print('converting file...')
                seen_boards = {eval(key): value for key, value in seen_boards.items()}
                print('done')
            except:
                pass
    except:
            pass

def ab_pruning_with_file(board, depth):  
    global seen_boards
    board_type = f"{board.width}x{board.height}x{board.in_a_row}"
    try:
        with open(f'./solved/{board_type}.json', 'r') as f:
            try:
                loaded_data = json.load(f)
                seen_boards = loaded_data
            except:
                pass
    except:
            pass
    print("starting search")
    results = ab_pruning(board, depth)
    print("ended search")
    with open(f'./solved/{board_type}.json', 'w') as file:
        json.dump(seen_boards, file, indent=4)
    return results
        

def ab_pruning(board, depth=-1, alpha=float("-inf"), beta=float("inf")):
    if depth == -1:
        depth = board.width*board.height
    global seen_boards
    
    legal_moves = board.generate_legal_moves()
    center_column = (board.width-1) // 2
    legal_moves.sort(key=lambda move: abs(move - center_column))
    
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
                    seen_boards[board_str] = eval[0]
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
                    seen_boards[board_str] = eval[0]
                
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
            start_time = time.time()
            move = ab_pruning(board, board.width*board.height)
            print ("My program took", time.time() - start_time, "to run")
            board.play_move(move[1])
            print("The AI has moved")
            print(f"AI Eval: {move[0]}")
        
            print(board.display_board())
    print(board.display_board())
    if board.isWin == 1:
        print(f"Player {(board.turn+1) % 2 + 1} won!")
    else: print(f"It is a tie!")

import time
board = Connect4Game(width=5, height=6, in_a_row =4)
ab_pruning_with_file(board, board.width*board.height)
#set_solved(board)
play_game_v_AI(board, 2)
# start_time = time.time()
# ab_pruning(board)
# print ("My program took", time.time() - start_time, "to run")
