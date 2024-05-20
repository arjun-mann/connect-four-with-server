import connectfour

def ask_columns() -> int:
    '''Asks users to specify how many columns they want in the game'''
    while True:
        cols = input("Number of columns: ")
        try:
            if int(cols) < 4 or int(cols) > 20:
                raise ValueError
            break
        except:
            print('Invalid input!')
    return int(cols)

def ask_rows() -> int:
    '''Asks users to specify how many rows they want in the game'''
    while True:
        rows = input("Number of rows: ")
        try:
            if int(rows) < 4 or int(rows) > 20:
                raise ValueError
            break
        except:
            print('Invalid input!')
    return int(rows)

def print_game(board:connectfour.GameState) -> None:
    '''Prints current game'''
    max_num_len = 1
    for i in range(1, len(board[0])+1):
        if len(str(i)) > max_num_len:
            max_num_len = len(str(i))
    displacement = max_num_len * ' '

    for i in range(1, len(board[0])+1):
        num_of_spaces_needed = max_num_len - (len(str(i+1))-1)
        displacement = ' ' * num_of_spaces_needed
        print(i, end = displacement)
    print()
    displacement = max_num_len * ' '
    for i in range(0, len(board[0][0])):
        for j in range(0, len(board[0])):
            if board[0][j][i] == connectfour.EMPTY:
                print('.', end = displacement)
            elif board[0][j][i] == connectfour.RED:
                print('R', end = displacement)
            elif board[0][j][i] == connectfour.YELLOW:
                print('Y', end = displacement)
        print()
        
def print_turn(board:connectfour) -> None:
    if board[1] == 1:
        print("It is Red's turn")
    elif board[1] == 2:
        print("It is Yellow's turn")