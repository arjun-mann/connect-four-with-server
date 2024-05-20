import connectfour
import common

def create_board(cols:int, rows:int) -> connectfour.GameState:
    '''Creates and returns GameState object using int cols and int rows'''
    return (connectfour.new_game(cols, rows))
    
def player_turn(board:connectfour.GameState) -> connectfour.GameState:
    '''Completes the current player's turn by updating and returning a GameState. Allows the user to DROP or POP
    a piece'''
    while True:
        try:
            move = input("Type a move type ('DROP' or 'POP'), then a space, then a number between 1 and " + str(cols) + ": ")
            lmove = move.split()
            if lmove[0] == 'DROP':
                board = connectfour.drop(board, int(lmove[1])-1)
                return board
            elif lmove[0] == 'POP':
                board = connectfour.pop(board, int(lmove[1])-1)
                return board
            else:
                raise ValueError
        except:
            print("Invalid input! Try again")

if __name__ == '__main__':
    cols = common.ask_columns()
    rows = common.ask_rows()
    board:connectfour.GameState = create_board(cols, rows)
    common.print_game(board)
    common.print_turn(board)
    while True:
        board = player_turn(board)
        common.print_game(board)
        if connectfour.winner(board) == 1:
            print("WINNER_RED")
            break
        if connectfour.winner(board) == 2:
            print("WINNER_YELLOW")
            break
        else:
            common.print_turn(board)
        