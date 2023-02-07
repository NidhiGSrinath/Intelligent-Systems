from functools import partial
import tkinter as tk
import copy
import time
 
class TicTacToe3D:
    def __init__(self) -> None:


        self.gameover = False # is set to true when a player wins or all blocks are used
        self.turn = 'X'  #first turn is set to 'X'
        self.player = 'X'
        self.depth = 2
        self.board = [[['' for c in range(0,4)] for r in range(0,4)] for f in range(0,4)] #initializing the board

        # initializing tkinter
        self.root = tk.Tk()  
        self.root.resizable(False, False)  
        self.root.title("Tic Tac Toe")

        # initializing the menu - first screen
        self.initial_menu = tk.Frame(self.root)
        self.initial_menu.pack(padx=50, pady=50)

        # initializing the board
        self.game_frame = tk.Frame(self.root)
        self.game_frame.pack(padx=1, pady=1)

        # setting the player symbol 
        tk.Label(self.initial_menu, text='Choose a player:', font=('Arial', 15)).pack(padx=1,pady=1)
        symbol = tk.IntVar(self.initial_menu,1)
        tk.Radiobutton(self.initial_menu, text="X", variable=symbol, value=1, font=('Arial', 12), command=partial(self.choose_player, 'X')).pack( anchor = 'w', padx= (200,0) )
        tk.Radiobutton(self.initial_menu, text="O", variable=symbol, value=2, font=('Arial', 12), command=partial(self.choose_player, 'O')).pack( anchor = 'w' , padx= (200,0))
        
        # setting the difficulty level
        tk.Label(self.initial_menu, text = "Difficulty:", font=('Arial', 15), width=10).pack(padx=1,pady=1)
        dif = tk.IntVar(self.initial_menu,1)
        tk.Radiobutton(self.initial_menu, text="Easy", variable=dif, value=1, font=('Arial', 12), command=partial(self.change_difficulty, 2)).pack( anchor = 'w' , padx= (200,0))
        tk.Radiobutton(self.initial_menu, text="Medium", variable=dif, value=2, font=('Arial', 12), command=partial(self.change_difficulty, 4)).pack( anchor = 'w' , padx= (200,0))
        tk.Radiobutton(self.initial_menu, text="Hard", variable=dif, value=3, font=('Arial', 12), command=partial(self.change_difficulty, 6)).pack( anchor = 'w' , padx= (200,0)) 
        
        # start button
        tk.Button(self.initial_menu, text='Start Game', font=('Arial', 15),  command=self.start_Game, bg='lightgreen').pack()
        self.root.mainloop() 

    # function for selecting who will have the first turn
    def choose_player(self, symbol):
        self.player = symbol

    # function to creates a copy of a board and generate a move
    def result(self,board,action,turn):
        newBoard = copy.deepcopy(board)
        f,r,c = action
        newBoard[f][r][c] = turn
        return newBoard

    # action of placing the symbol in one of the 64 positions by AI or human
    def actions(self, board):
        actions = []
        for f in range(0, 4):
            for r in range(0, 4):
                for c in range(0, 4):
                    if board[f][r][c]=='':
                        actions.append((f,r,c))
        return actions
    
    
    # function for AI to move and find optimal move based on the depth and minimax
    def AI_move(self): 
        self.nodes_visited = 0   
        if not self.gameover:    
            bestMove:any
            best = -1000
            for action in self.actions(self.board):
                next=self.result(self.board, action, self.turn)
                val = self.alphaBeta(next,'X' if self.turn=='O'else 'O',self.depth-1 ,False)
                if val >= best:
                    best = val
                    bestMove = action
                
            f,r,c = bestMove
            self.buttons[f][r][c].configure(text=self.turn, bg='lightblue'if self.turn=='X' else 'lightgreen', fg='black')
            self.board[f][r][c] = self.turn 

            if self.turn == "X":
                    self.turn = "O"
            elif self.turn == "O":
                    self.turn = "X"

            self.turn_label.configure(text= "Player turn" if self.turn==self.player else "AI turn")
            self.check_gameover(self.board, False)
            print('      nodes visited:',self.nodes_visited)
            print('Player Turn')

    # function that implements alpha beta and minimax
    def alphaBeta(self ,board, turn, depth, maximize = True, alpha = -1000, beta = 1000):
        self.nodes_visited+=1
        if depth == 0 or self.check_gameover(board):
            return self.value(board) + depth

        if maximize:
            best = -1000
            for action in self.actions(board):
                next = self.result(board, action, turn)
                val = self.alphaBeta(next,'X' if turn=='O'else 'O', depth-1,False, alpha, beta )
                best = max(best,val)
                alpha = max(alpha,best)

                if beta <= alpha:
                    break
            
            return alpha
        else:
            best = 1000
            for action in self.actions(board):
                next = self.result(board, action, turn)
                val = self.alphaBeta(next,'X' if turn=='O'else 'O', depth-1, True, alpha, beta)
                best = min(best, val)
                beta = min(beta, best)

                if beta <= alpha:
                    break
            
            return beta

    
    # function for recording player's move
    def player_move(self,data):
        if not self.gameover:
            self.turn_label.configure(text="AI turn")
            f, r, c = data
            
            if self.board[f][r][c] == '' and self.turn==self.player:
                self.buttons[f][r][c].configure(text=self.turn, bg='lightblue'if self.turn=='X' else 'lightgreen', fg='black')
                self.board[f][r][c] = self.turn 
                if self.turn == "X":
                    self.turn = "O"
                elif self.turn == "O":
                    self.turn = "X"
                

                self.check_gameover(self.board, False)
                print('AI Turn, ', end='')
                self.AI_move()

    
    # setting dificulty level
    def change_difficulty(self, difficulty):
        self.depth = difficulty

    # functio to start the game
    def start_Game(self):

        # reset the menu
        self.initial_menu.destroy()


        # re-initialize the menu, board and menu
        self.menu_area = tk.Frame(self.game_frame, width=150)
        self.menu_area.grid(row=0, column=0)

        self.play_area = tk.Frame(self.game_frame, width=400, height=550, bg='gray')
        self.play_area.grid(row=0, column=1)

        tk.Label(self.menu_area, text = "Tic Tac Toe", font=('Arial', 17)).pack(padx=1,pady=1)
        self.turn_label = tk.Label(self.menu_area, text = "Player's turn" if self.turn==self.player else "AI's turn", font=('Arial', 8), fg='blue'if self.turn=='O' else 'green')
        self.turn_label.pack(padx=5,pady=0)

        

        self.frames = []
        for f in range(0,4):
            frame = tk.Frame(self.play_area, width=100, height=100, bg='white')
            frame.grid(row=f, column=0)
            frame.grid_configure(padx=20,pady=3)
            self.frames.append(frame)


        self.buttons = []
        for f in range(0, 4):
            self.buttons.append([])
            for r in range(0, 4):
                self.buttons[f].append([])
                for c in range(0, 4):
                    button = tk.Button(self.frames[f], text="", width=f+2, height=1, command=partial(self.player_move, (f,r,c)))
                    button.grid(row=r, column=c)
                    self.buttons[f][r].append(button)

        if self.turn!=self.player:
            self.AI_move()
    
    # function to check the board to see wether it has the winning combinations
    def utility(self, board):
        for i in range(0, 4):
            for j in range(0, 4):

                # win combinations

                #horizontallly and vertically
                if board[i][j][0]!='':
                    if board[i][j][0] == board[i][j][1] == board[i][j][2] == board[i][j][3]:
                        return 1 if board[i][j][0] == 'X' else -1
                
                if board[i][0][j]!='':
                    if board[i][0][j] == board[i][1][j] == board[i][2][j] == board[i][3][j]:
                        return 1 if board[i][0][j] == 'X' else -1

                if board[0][i][j]!='':
                    if board[0][i][j] == board[1][i][j] == board[2][i][j] == board[3][i][j]:
                        return 1 if board[0][i][j] == 'X' else -1

                #diagonally from left to right
                if board[i][0][0]!='':
                    if board[i][0][0] == board[i][1][1] == board[i][2][2] == board[i][3][3]:
                        return 1 if board[i][0][0] == 'X' else -1

                if board[0][i][0]!='':
                    if board[0][i][0] == board[1][i][1] == board[2][i][2] == board[3][i][3]:
                        return 1 if board[0][i][0] == 'X' else -1
                
                if board[0][0][i]!='':
                    if board[0][0][i] == board[1][1][i] == board[2][2][i] == board[3][3][i]:
                        return 1 if board[0][0][i] == 'X' else -1

                #diagonally from right to left
                if board[i][0][3]!='':
                    if board[i][0][3] == board[i][1][2] == board[i][2][1] == board[i][3][0]:
                        return 1 if board[i][0][3] == 'X' else -1

                if board[0][i][3]!='':
                    if board[0][i][3] == board[1][i][2] == board[2][i][1] == board[3][i][0]:
                        return 1 if board[0][i][3] == 'X' else -1

                if board[0][3][i]!='':
                    if board[0][3][i] == board[1][2][i] == board[2][1][i] == board[3][0][i]:
                        return 1 if board[0][3][i] == 'X' else -1
            
            if board[i][i][0]!='':
                if board[i][i][0] == board[i][i][1] == board[i][i][2] == board[i][i][3]:
                    return 1 if board[i][i][0] == 'X' else -1

            if board[i][0][i]!='':
                if board[i][0][i] == board[i][1][i] == board[i][2][i] == board[i][3][i]:
                    return 1 if board[i][0][i] == 'X' else -1

            if board[0][i][i]!='':
                if board[0][i][i] == board[1][i][i] == board[2][i][i] == board[3][i][i]:
                    return 1 if board[0][i][i] == 'X' else -1

        if board[0][0][0]!='':
            if board[0][0][0] == board[1][1][1] == board[2][2][2] == board[3][3][3]:
                return 1 if board[0][0][0] == 'X' else -1
        
        if board[0][0][3]!='':
            if board[0][0][3] == board[1][1][2] == board[2][2][1] == board[3][3][0]:
                return 1 if board[0][0][3] == 'X' else -1
        
        return 0
    
    

    # check if a win condition is satisfied
    def check_gameover(self,board, inExploration = True):
        if self.utility(board)!=0 or len(self.actions(board))==0:
            if not inExploration:
                self.gameover = True
                self.updateStatus()


    # update the status on the board and display the winner
    def updateStatus(self):
        u = self.utility(self.board)

        if u == 1:
            tk.Label(self.root, text='GAME OVER - X won', font=('Arial', 15)).pack(padx=1,pady=1)
        elif u == -1:
            tk.Label(self.root, text='GAME OVER - O won', font=('Arial', 15)).pack(padx=1,pady=1)
        elif len(self.actions(self.board))==0:
            tk.Label(self.root, text='GAME OVER - Draw', font=('Arial', 15)).pack(padx=1,pady=1)


    # gets the value for the AI's next move based on the difficulty level
    def value(self, board):
        if self.utility(board) == 1:
            return 1000 if self.player == 'O' else -1000
        elif self.utility(board) == -1:
            return 1000 if self.player == 'X' else -1000

        score = 0

        for i in range(0, 4):
            for j in range(0, 4):

                #horizontally and vertically
                if board[i][j][0]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[i][j][v] == 'X':
                            have_X =True
                        elif board[i][j][v] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1
                
                if board[i][0][j]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[i][v][j] == 'X':
                            have_X =True
                        elif board[i][v][j] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                if board[0][i][j]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[v][i][j] == 'X':
                            have_X =True
                        elif board[v][i][j] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                #diagonally from left to right
                if board[i][0][0]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[i][v][v] == 'X':
                            have_X =True
                        elif board[i][v][v] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                if board[0][i][0]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[v][i][v] == 'X':
                            have_X =True
                        elif board[v][i][v] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1
                
                if board[0][0][i]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[v][v][i] == 'X':
                            have_X =True
                        elif board[v][v][i] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                #diagonally from right to left
                if board[i][0][3]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[i][v][3-v] == 'X':
                            have_X =True
                        elif board[i][v][3-v] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                if board[0][i][3]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[v][i][3-v] == 'X':
                            have_X =True
                        elif board[v][i][3-v] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1

                if board[0][3][i]!='':
                    have_X = False
                    have_O = False
                    for v in range(0,4):
                        if board[v][3-v][i] == 'X':
                            have_X =True
                        elif board[v][3-v][i] == 'O':
                            have_O = True
                    if not have_X:
                        score -=1
                    if not have_O:
                        score +=1
            
            if board[i][i][0]!='':
                have_X = False
                have_O = False
                for v in range(0,4):
                    if board[i][i][v] == 'X':
                        have_X =True
                    elif board[i][i][v] == 'O':
                        have_O = True
                if not have_X:
                    score -=1
                if not have_O:
                    score +=1

            if board[i][0][i]!='':
                have_X = False
                have_O = False
                for v in range(0,4):
                    if board[i][v][i] == 'X':
                        have_X =True
                    elif board[i][v][i] == 'O':
                        have_O = True
                if not have_X:
                    score -=1
                if not have_O:
                    score +=1

            if board[0][i][i]!='':
                have_X = False
                have_O = False
                for v in range(0,4):
                    if board[v][i][i] == 'X':
                        have_X =True
                    elif board[v][i][i] == 'O':
                        have_O = True
                if not have_X:
                    score -=1
                if not have_O:
                    score +=1

        if board[0][0][0]!='':
            have_X = False
            have_O = False
            for v in range(0,4):
                if board[v][v][v] == 'X':
                    have_X =True
                elif board[v][v][v] == 'O':
                    have_O = True
            if not have_X:
                score -=1
            if not have_O:
                score +=1
        
        if board[0][0][3]!='':
            have_X = False
            have_O = False
            for v in range(0,4):
                if board[v][v][3-v] == 'X':
                    have_X =True
                elif board[v][v][3-v] == 'O':
                    have_O = True
            if not have_X:
                score -=1
            if not have_O:
                score +=1
    
        return score if self.player == 'O' else -score


# calling the game method
game = TicTacToe3D()
