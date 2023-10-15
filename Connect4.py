class Connect4Game:
    
    def __init__(self, mode=0, width=7, height=6, in_a_row=4):
        self.mode = 0
        
        self.width = width
        self.height = height
        self.in_a_row = in_a_row
                
        self.isWin = 0 #turns 1 if true, 2 if tie
        
        self.tops = []
        self.tie_check = [] #array that if tops = tie_check, its a tie
        
        self.moves = []
        for col in range(self.width):
            self.tie_check.append(self.height)
            self.tops.append(0)
        
        self.relevent_board = []
        self.board = [] # board is board[col][row]
        for col in range(self.width):
            arr = []
            for item in range(self.height):
                arr.append(0)
            self.board.append(arr)
            self.relevent_board.append(arr)
            
        
        self.turn = 0 #0 -> P1, 1 -> P2
            
            
        
        self.mode = mode
    
    def set_relevent_boards(self):
        for col in range(len(self.board)):
            for row in range(len(self.board[col])):
                if self.board[col][row] != 0:
                    in_range = False
                    for i in range(len(self.tops)):
                        dist_in_height = abs((self.tops[i]-row))
                        dist_in_width = abs(col-i)
                        if max(dist_in_height, dist_in_width) < self.in_a_row:
                            in_range = True
                    if in_range == False:
                        self.relevent_board[col][row] = 3
                    else:
                        self.relevent_board[col][row] = self.board[col][row]


            #modes:
         # 0 -> PvP
         # 1 -> P v AI
         # 2 -> AI v AI

    def play_move(self, col):
        
        #give array of moves for quick testing
        if type(col) is list:
            for move in col:
                self.play_move(move)
            return
        #col starts at 0!
        if col < 0 or col >= self.width:
            if self.mode != 2:
                print(f"Keep the move within 0 -> {self.width-1}. Play Again.")
            return

        if self.tops[col] > self.height-1:
            print(f"Move went over the board. Play Again.")
            return
        
        if self.isWin != 0:
            print("Game is over.")
            return

        self.board[col][self.tops[col]] = self.turn + 1 # turn + 1 makes it into player number
        
        self.moves.append(col)
        self.tops[col] += 1        
        self.turn = (self.turn + 1) % 2
        self.detectWasWin()
        self.set_relevent_boards()
        
       
    def detectWasWin(self):
        
        
        
        col = self.moves[-1]
        row = self.tops[col]-1
        player_moved = (self.turn + 1) % 2
        #last played move info^^
        left = self.count_in_dir(col, row, player_moved, -1, 0)
        right = self.count_in_dir(col, row, player_moved, 1, 0)
        
        down = self.count_in_dir(col, row, player_moved, 0, -1)
        down_left = self.count_in_dir(col, row, player_moved, -1, -1)
        up_right = self.count_in_dir(col, row, player_moved, 1, 1)
        
        up_left = self.count_in_dir(col, row, player_moved, -1, 1)
        down_right = self.count_in_dir(col, row, player_moved, 1, -1)
        
        if left + right >= self.in_a_row-1:
            self.isWin = 1
        if down + 0 >= self.in_a_row-1:
            self.isWin = 1
        
        if down_left + up_right >= self.in_a_row-1:
            self.isWin = 1
    
        if up_left + down_right >= self.in_a_row-1:
            self.isWin = 1
        
        if self.generate_legal_moves() == [] and self.isWin != 1:
            self.isWin = 2

        return self.isWin
    
    #count in a direction based on off sets (-1, 0, 1) in col and row
    def count_in_dir(self, col, row, player, offset_col, offset_row):
        #if square looked if off board
        new_col = col + offset_col
        new_row = row + offset_row
        if new_col < 0 or new_col >= self.width:
            return 0
        if new_row < 0 or new_row >= self.height:
            return 0        
        
        if self.board[new_col][new_row] == player+1:
            #print("counted" + str(len(self.moves)) + " player " + str(player+1))
            return 1 + self.count_in_dir(new_col, new_row, player, offset_col, offset_row)
        else:
            return 0
        
    def playHumanGame(self):
        print(self.display_board())
        if self.mode == 0:
            while self.isWin == 0:
                self.play_move(int(input(f"Player {self.turn+1}, it is your move. Type 0 -> {self.width-1}: ")))
                print(self.display_board(board_type="relevent"))
            if self.isWin == 1:
                print(f"Player {(self.turn+1) % 2 + 1} won!")
            else: print(f"It is a tie!")
    
    def generate_legal_moves(self):
        legal_moves = []
        for col in range(self.width):
            if self.tops[col] != self.height:
                legal_moves.append(col)
        return legal_moves
                
    
    def display_board(self, board_type="normal"):
        display = ""
        used_board = None
        if board_type == "normal":
            used_board = self.board
        elif board_type == "relevent":
            used_board=self.relevent_board



        #Loop through height, and then cols
        for i in range(self.height):
            for j in range(self.width):
                display += "+---"
            display += "+ \n"
            for j in range(self.width):
                display += "| "
                val = used_board[j][self.height-1-i]
                dis_item = ""
                if val == 0:
                    dis_item = " "
                elif val == 1:
                    dis_item = "A"
                elif val == 2: 
                    dis_item = "B"
                else:
                    dis_item = "."
                display += dis_item + " "
            display+= "| \n"
        for j in range(self.width):
            display += "+---"
        display += "+ \n"


        for j in range(self.width):
            display += f"  {j} "
        display += "\n"

        return display

        
    
game = Connect4Game()
game.playHumanGame()
