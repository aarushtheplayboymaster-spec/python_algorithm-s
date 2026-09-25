#Tic-Tac-Toe logic
import math
import random
class TIC_TAC_TOE_BOARD:
    def __init__(self):
        self.gameisrunning = True
        self.player1 = True
        self.maxplayer = 'X'
        self.miniplayer = 'O'
        self.board = [" "," "," "," "," "," "," "," "," "]
        self.winning_con = [[0,1,2],[3,4,5],[6,7,8],
                            [0,3,6],[1,4,7],[2,5,8],
                            [0,4,8],[2,4,6]]



    def TTT_board(self):
        print(f" {self.board[0]} | {self.board[1]} | {self.board[2]}")
        print("-----------")
        print(f" {self.board[3]} | {self.board[4]} | {self.board[5]}")
        print("-----------")
        print(f" {self.board[6]} | {self.board[7]} | {self.board[8]}")
    #tic-tac-toe hecuristic checks win, lose and tie
    def hecuristic(self):
        for a,b,c in self.winning_con:
            if self.board[a] == self.board[b] == self.board[c] and self.board[c] != ' ':
                return 1 if self.board[a] == self.maxplayer else -1
        return 0
    def game_is_over(self):
        return self.hecuristic() != 0 or ' ' not in self.board
    #this gives all the empty spots.
    def get_legal_moves(self):
        return [i for i,spot in enumerate(self.board) if spot == " "]

    def wining_codetion(self):
            if self.game_is_over():
                self.gameisrunning = False
                final_score = self.hecuristic()
                if final_score == 1:
                    print("Ai has won")
                elif final_score == -1:
                    print("player has won")
                else:
                    print("It's a draw")
                return True
            return False


    def player_control(self):
        if self.player1 == True:
            while True: 
                max_player_input = int(input('ENTER A NUMBER 0-8:- '))
                if 0 <= max_player_input <=8 and self.board[max_player_input] == ' ':
                    self.board[max_player_input] = self.miniplayer
                    break
                print('you can not play that')
            self.TTT_board()
            self.wining_codetion()
            self.player1 = False
    def simulat_moves(self,move):
        state = TIC_TAC_TOE_BOARD()
        state.board = list(self.board)
        state.player1 = not self.player1
        current_sing = self.maxplayer if self.player1 else self.miniplayer
        state.board[move] = current_sing
        return state

#MCTS engine
class MCTS:
    def __init__(self,board, parent = None,move = None):
        self.state = board
        self.parent = parent
        self.move = move
        self.children = []
        self.number_of_wins = 0
        self.number_of_visite = 0
        self.untried_moves = board.get_legal_moves()

#this calculates the best node to visite
    def get_UCB1_score(self,exploration_constant=1.414):
        if self.number_of_visite == 0:
            return float('inf')
        
        exploitation = self.number_of_wins / self.number_of_visite
        exploration = exploration_constant * math.sqrt(math.log(self.parent.number_of_visite ) / self.number_of_visite)
        return exploitation + exploration
#this uses UCB1_score and choose the best node
    def select(self):
        current_node = self
        while not current_node.untried_moves and not current_node.state.game_is_over():
            current_node = max(current_node.children,key=lambda child: child.get_UCB1_score())
        return current_node
#when select() find that there are untried moves it makes the node, child_node and appends them in childern   
    def expand(self):
        if self.untried_moves:
            move = self.untried_moves.pop()
            new_board = self.state.simulat_moves(move)
            child = MCTS(board=new_board,parent=self,move=move)
            self.children.append(child)
            return child
    def simulate(self):
        current_board = self.state
        while not current_board.game_is_over():
            right_move = current_board.get_legal_moves()
            random_move = random.choice(right_move)
            current_board = current_board.simulat_moves(random_move)
        return current_board.hecuristic()
    def backtrack(self,result):
        current_node = self
        while current_node is not None:
            current_node.number_of_visite += 1
            current_node.number_of_wins += result
            current_node = current_node.parent
    def mcts_search(self,loop_runs=1000):
        for _ in range(loop_runs):
            node = self.select()
            if node.untried_moves and not node.state.game_is_over():
                node = node.expand() 
            result = node.simulate()
            node.backtrack(result)
        best_path = max(self.children,key=lambda child: child.number_of_visite)
        return best_path.move

game_board = TIC_TAC_TOE_BOARD()
while game_board.gameisrunning:
    game_board.player_control()
    if not game_board.gameisrunning:
        break
    root = MCTS(game_board)
    ai_move = root.mcts_search()
    game_board.board[ai_move] = game_board.maxplayer
    game_board.TTT_board()
    game_board.wining_codetion()
    game_board.player1 = True








 