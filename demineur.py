import random
from colorama import Fore, Back, Style, init
import tkinter
init()

random.seed(420)
def create_board(n, m):
    board = [["*"]*n for i in range(m)]
    return board


def print_board(board ):

    for t in range(len(board)) :
        if t == 0 :
            print("      ", end= "")
            for x in range(len(board[0])) :
                if x >= 10 :
                    print(x, end= " ")
                else :
                    print(x, end= "  ")


            print( "")
        for c in range(len(board[0])):
            if c == 0 :
                if t >= 10 :
                    print(t, "|", end= "  ")
                else :
                    print("",t, "|", end= "  ")
            pos = board[t][c]
            if pos == "X" :
                print(Fore.RED + Style.BRIGHT+ str(pos), end= "  ")
            elif pos == 1 :
                print(Fore.CYAN + str(pos), end="  ")
            elif pos == 2:
                print(Fore.BLUE + str(pos), end="  ")
            elif pos == 3:
                print(Fore.RED+ Style.BRIGHT + str(pos), end="  ")
            else :
                print(Style.RESET_ALL+ str(board[t][c]), end= "  ")
        print(Style.RESET_ALL + "")



def get_neigboard(board, pos_xy ):
    alentour_liste = []
    for x in range(pos_xy[0] - 1, pos_xy[0] + 2):
        for y in range(pos_xy[1] -1, pos_xy[1] + 2) :
            if  (x < len(board[0])  and y < len(board)) and x >= 0 and y >= 0 :
                alentour_liste.append((x, y))

    return alentour_liste


def place_mine(refferance_board, start_pos):
    list_of_bomb = []
    get_list = get_neigboard(refferance_board, start_pos)
    for i in range(25) :
        bombo = True
        while bombo :
            mine = (random.randint(0, len(refferance_board[0] ) -1),random.randint(0, len(refferance_board[0]) -1))
            if mine != start_pos and mine not in list_of_bomb and mine  not in get_list:
                list_of_bomb.append(mine)
                refferance_board[mine[0]][mine[1]] = "X"
                bombo = False

    return list_of_bomb

def fill_in_board(refferance_board) :
    for i in range(len(refferance_board)) :
        for c in range(len(refferance_board[0])) :
            compt = 0
            get_list = get_neigboard(refferance_board, (i, c))
            for t in get_list :
                if refferance_board[t[0]][t[1]] == "X" :
                    compt += 1
            if refferance_board[i][c] != "X" :
                refferance_board[i][c] = compt


    return get_list
def propagation_click(board, refferance_board, pos_xy) :
    visited_point = create_board(len(board), len(board[0]))
    propagation_click_recursion(board, refferance_board, pos_xy, visited_point)



def propagation_click_recursion(board, refferance_board, pos_xy, vissited_point) :
    if vissited_point[pos_xy[0]][pos_xy[1]] != "*" :
        return
    vissited_point[pos_xy[0]][pos_xy[1]] = "T"
    get_list = get_neigboard(refferance_board, pos_xy)
    zero_list = []
    for elem in get_list :

        if refferance_board[elem[0]][elem[1]] == 0:
            board[elem[0]][elem[1]] = 0
            zero_list.append(elem)
        if refferance_board[elem[0]][elem[1]] != "X":
            board[elem[0]][elem[1]] = refferance_board[elem[0]][elem[1]]
    if len(zero_list) > 0 :
        for zero in zero_list :
            propagation_click_recursion(board, refferance_board, zero, vissited_point)


def input_jouer(bool, board) :
    inpu = True
    while inpu :
        if bool :
            input_user = input( "y : ")
        else :
            input_user = input( "x : ")

        try :
            val = int(input_user)
            if 0 <= int(input_user) and  int(input_user) <= len(board[0]) -1 :
                 inpu = False
        except ValueError :
            inpu = True

    return int(input_user)


def check_win(board, refferance_board, list_of_mine, list_of_flag, tuple_user) :
    bool1 = True
    bool2 = True
    if refferance_board[tuple_user[0]][tuple_user[1]] == "X" :
        for mine in list_of_mine :
            board[mine[0]][mine[1]] = "X"

        bool1 = False
    if len(list_of_flag) > 0 :
        new_flag = list_of_flag.sort()
        new_mine = list_of_mine.sort()
        print(new_flag)
        print(new_mine)


    return (bool1, bool2)


def main() :
    list_of_mine = []
    list_of_flag = []
    board = create_board(12, 12 )
    refferance_board = create_board(12, 12)
    print_board(board)

    input_userx = input_jouer(True, board)
    input_usery = input_jouer(False, board)




    tuple_user = (input_userx, input_usery)
    list_of_mine = place_mine(refferance_board, tuple_user)
    fill_in_board(refferance_board)
    print_board(refferance_board)
    propagation_click(board, refferance_board, tuple_user )
    print_board(board)
    win_check = check_win(board, refferance_board, list_of_mine, list_of_flag, tuple_user)
    while win_check[0] :
        input_drap = input("F for flag, X for nothing : ")
        if input_drap == "F":
            drap_x = input_jouer(True, board)
            drap_y = input_jouer(False, board)
            board[drap_x][drap_y] = Fore.GREEN + "F"
            list_of_flag.append((drap_x,drap_y))
            print_board(board)
        else :
            input_userx = input_jouer(True, board)
            input_usery = input_jouer(False, board)


            tuple_user = (input_userx, input_usery)
            if refferance_board[tuple_user[0]][tuple_user[1]] == 0:
                propagation_click(board, refferance_board, tuple_user)
            else :
                board[tuple_user[0]][tuple_user[1]] = refferance_board[tuple_user[0]][tuple_user[1]]
            win_check = check_win(board, refferance_board, list_of_mine, list_of_flag, tuple_user)
            print_board(board)
    if win_check[1] == True :
        print("perdu \n vous etes tomber sur une mine ")

main()