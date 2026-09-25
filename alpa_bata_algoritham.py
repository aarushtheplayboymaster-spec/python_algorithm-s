#the tic-tac-toe game
import math
import time
gameisrunning = True
player1 = True
maxplayer = 'X'
miniplayer = 'O'
board = [" "," "," "," "," "," "," "," "," "]
winning_con = [[0,1,2],[3,4,5],[6,7,8],
                [0,3,6],[1,4,7],[2,5,8],
                [0,4,8],[2,4,6]]
player_choise = input('choise PLAYERvsAI/AIvsAI:- ')
def TTT_board(board):
    print(f" {board[0]} | {board[1]} | {board[2]}")
    print("-----------")
    print(f" {board[3]} | {board[4]} | {board[5]}")
    print("-----------")
    print(f" {board[6]} | {board[7]} | {board[8]}")
#tic-tac-toe hecuristic

def hecuristic(board,winning_con):
    for a,b,c in winning_con:
        if board[a] == board[b] == board[c] and board[c] != ' ':
            return 10 if board[a] == maxplayer else -10
    return 0
def game_is_over(board):
    return hecuristic(board,winning_con) or ' ' not in board

#children nodes
def get_children(board, symbol):
    children = []
    for i in range(len(board)):
        if board[i] == ' ':
            new_board = list(board)
            new_board[i] = symbol
            children.append((i,new_board))
    return children

#the core Minimax algorithm 
def alpa_bata(board,alpa,bata,depth,is_maxing):
    if game_is_over(board) or depth==0:
        return hecuristic(board,winning_con)
    if is_maxing:
        max_val = -math.inf
        for _,child_board in get_children(board,maxplayer):
            eval = alpa_bata(child_board,alpa,bata,depth-1,False)
            max_val = max(max_val,eval)
            alpa = max(alpa,eval)
            if alpa >= bata:
                break
        return max_val
    else:
        min_val = math.inf
        for _,child_board in get_children(board,miniplayer):
            eval = alpa_bata(child_board,alpa,bata,depth-1,True)
            min_val = min(min_val,eval)
            bata = min(bata,eval)
            if alpa >= bata:
                break
        return min_val
    
#best move finder
def best_move_finderX(board):
    best_score = -math.inf
    best_move = -1
    for board_indax,child_board in get_children(board,maxplayer):
        score = alpa_bata(child_board,alpa= -math.inf ,bata = math.inf ,depth=9,is_maxing=False)
        if score > best_score:
            best_score = score
            best_move = board_indax
    return best_move
def best_move_finderO(board):
    best_score = math.inf
    best_moveO = -1
    for board_indax,child_board in get_children(board,miniplayer):
        score = alpa_bata(child_board,depth=9,is_maxing=True)
        if score < best_score:
            best_score = score
            best_moveO = board_indax
    return best_moveO
def wining_codetion(board):
        global gameisrunning
        if game_is_over(board):
            gameisrunning = False
            final_score = hecuristic(board,winning_con)
            if final_score == 10:
                print("Ai has won")
            elif final_score == -10:
                print("player has won")
            else:
                print("It's a draw")
            return True
        return False
def player_control(board):
    global player1
    if player1 == True:
        max_player_input = int(input('ENTER A NUMBER 0-8:- '))
        if board[max_player_input] != ' ':
            print('you can not play that')
        board[max_player_input] = miniplayer
        TTT_board(board)
        player1 = False
        wining_codetion(board)

    if player1 == False:
        print("it\'s AI'S TURN")
        AI_move = best_move_finderX(board)
        if board[AI_move] != -1:
            board[AI_move] = maxplayer
        TTT_board(board)
        player1 = True
        wining_codetion(board)
def AI_simulation(board):
    global player1
    if player1 == True:
        print("it\'s AI'S TURN")
        AI_moveO = best_move_finderO(board)
        if board[AI_moveO] != -1:
            board[AI_moveO] = miniplayer
        TTT_board(board)
        time.sleep(1)
        player1 = False
        wining_codetion(board)

    if player1 == False:
        print("it\'s AI'S TURN")
        AI_move = best_move_finderX(board)
        if board[AI_move] != -1:
            board[AI_move] = maxplayer
        TTT_board(board)
        time.sleep(1)
        player1 = True
        wining_codetion(board)

TTT_board(board)
if player_choise == "PLAYERvsAI":
    while gameisrunning:
        player_control(board)
elif player_choise == "AIvsAI":
    while gameisrunning:
        AI_simulation(board)