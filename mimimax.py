from Connect4 import Connect4Game

def max_of_tuple(arr):
    maxi_index = 0
    for item in range(len(arr)):
        if arr[item][0] > arr[maxi_index][0]:
            maxi_index = item
    return arr[maxi_index]

def min_of_tuple(arr):
    mini_index = 0
    for item in range(len(arr)):
        if arr[item][0] < arr[mini_index][0]:
            mini_index = item
    return arr[mini_index]


seen_boards = {

}


#Returns best score, and the move associated with it ((score, move), all possible moves)
def minimax(board: Connect4Game, depth):
    global seen_boards
    legal_moves = board.generate_legal_moves()
    if board.isWin == 1:
        if (board.turn + 1) % 2:
            return ((-1*(depth+1), board.moves[-1]), [])
        else:
            return ((1*(depth+1), board.moves[-1]), [])

    if len(legal_moves) == 0:
        return ((0, board.moves[-1]), [])

    if depth != 0:
        next_games = []
        
        for move in range(len(legal_moves)):
            new_board = Connect4Game()

            new_board.play_move(board.moves + [legal_moves[move]])

            new_board_array = new_board.board
            score = 0
            tuple_of_tuples = tuple(tuple(sublist) for sublist in new_board_array)
            if tuple_of_tuples in seen_boards:
                score = seen_boards[tuple_of_tuples]
            else:
                score = minimax(new_board, depth-1)[0][0]
                seen_boards[tuple_of_tuples] = score


            next_games.append((score, legal_moves[move]))
        if board.turn == 0:
            return (max_of_tuple(next_games), next_games)
        else:
            return (min_of_tuple(next_games), next_games)
        
    
def play_game_v_AI(board, player):
    print(board.display_board())
    while board.isWin == 0:
        #0 means human player 1, 1 means AI player 2
        if board.turn == player-1:
            board.play_move(int(input(f"Player {board.turn+1}, it is your move. Type 0 -> {board.width-1}: ")))
            move = minimax(board, board.width*board.height)
        else:
            move = minimax(board, board.width*board.height)
            board.play_move(move[0][1])
            print("The AI has moved")
        
            print(board.display_board())
    print(board.display_board())
    if board.isWin == 1:
        print(f"Player {(board.turn+1) % 2 + 1} won!")
    else: print(f"It is a tie!")

            
start = Connect4Game()

play_game_v_AI(start, player=1)
    

#print(minimax(start, 3))


