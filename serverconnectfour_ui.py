import serverconnectfour
import connectfour
import common

I32CFSP_HOST = 'circinus-32.ics.uci.edu'
I32CFSP_PORT = 4444


def run_user_interface() -> None:
    '''Runs the console-mode user interface from start to finish.'''
    _show_welcome_banner()
    connection = serverconnectfour.connect(I32CFSP_HOST, I32CFSP_PORT)

    try:
        _login(connection)  
        board = _create_board_ui(connection)
        while True:
            board = player_turn(connection, board)
            common.print_game(board)
            if check_win(board) == True:
                break
            board = serverconnectfour.read_server_move(connection, board)
            common.print_game(board)
            if check_win(board) == True:
                break
    finally:
        serverconnectfour.close(connection)

def _create_board_ui(connection: connectfour.GameState) -> connectfour.GameState:
    '''Asks the user to specify columns and rows to create a GameState, and gives 
    an initial print before returning the GameState'''
    cols = common.ask_columns()
    rows = common.ask_rows()
    board = connectfour.new_game(cols, rows)
    serverconnectfour.help_server_create(connection, board)
    common.print_game(board)
    return board
    
    
def check_win(board: connectfour.GameState) -> bool:
    '''Checks whether there is a winner to the game'''
    if connectfour.winner(board) == 1:
        print("WINNER_RED")
        return True
    if connectfour.winner(board) == 2:
        print("WINNER_YELLOW")
        return True
    else:
        common.print_turn(board)
        return False

def player_turn(connection, board) -> connectfour.GameState:
    '''Completes the current player's turn'''
    while True:
        lmove = []
        try:
            move = input("Type a move type ('DROP' or 'POP'), then a space, then a number between 1 and " + str(connectfour.columns(board)) + ": ")
            lmove = move.split()
            if lmove[0] == 'DROP':
                board = connectfour.drop(board, int(lmove[1])-1)
                break
            elif lmove[0] == 'POP':
                board = connectfour.pop(board, int(lmove[1])-1)
                break
            else:
                raise ValueError
        except:
            print("Invalid input! Try again")
    assert serverconnectfour.provide_server_turn(connection, lmove) == True
    return board
    
def _login(connection: serverconnectfour.I32CFSPConnection) -> None:
    '''Asks the user for a username and then attempts to log in with that
    username.  This repeats until the username is accepted by the server.
    '''
    while True:
        username = _ask_for_username()

        if serverconnectfour.hello(connection, username):
            return
        else:
            print('That user does not exist')
            
def _ask_for_username() -> str:
    '''Asks the user to enter a username and returns it as a string.  Continues
    asking repeatedly until the user enters a username that is non-empty, as
    the serverconnectfour server requires.
    '''
    while True:
        username = input('Username: ')
        try:
            if len(username) > 0:
                return username
            else:
                raise ValueError
        except:
            print("Invalid username! Try again")
            
def _show_welcome_banner() -> None:
    '''
    Shows the welcome banner
    '''
    print('Welcome to the serverconnectfour client!')
    print()

if __name__ == '__main__':
    run_user_interface()
    

