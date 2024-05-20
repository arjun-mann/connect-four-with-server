from collections import namedtuple
import socket
import connectfour

_SHOW_DEBUG_TRACE = False

I32CFSPConnection = namedtuple(
    'I32CFSPConnection',
    ['socket', 'input', 'output'])

class I32CFSPProtocolError(Exception):
    pass

def connect(host: str, port: int) -> I32CFSPConnection:
    '''
    Connects to a I32CFSP server running on the given host and listening
    on the given port, returning a I32CFSP Connection object describing
    that connection if successful, or raising an exception if the attempt
    to connect fails.
    '''
    I32CFSP_socket = socket.socket()
    
    I32CFSP_socket.connect((host, port))

    I32CFSP_input = I32CFSP_socket.makefile('r')
    I32CFSP_output = I32CFSP_socket.makefile('w')

    return I32CFSPConnection(
        socket = I32CFSP_socket,
        input = I32CFSP_input,
        output = I32CFSP_output)
    
def hello(connection: I32CFSPConnection, username: str) -> bool:
    '''Logs a user into the I32CFSP service over a previously-made connection.
    Returns True if logging in was successful (i.e., the user existed),
    False if the user did not exist
    '''
    _write_line(connection, f'I32CFSP_HELLO {username}')

    response = _read_line(connection)

    if response == f'WELCOME {username}':
        return True
    elif response.startswith('NO_USER '):
        return False
    else:
        raise I32CFSPProtocolError()
    
def help_server_create(connection: I32CFSPConnection, board: connectfour.GameState) -> None:
    '''Informs server of the GameState dimensinos when a new game is starting, and ensures server responds
    with "READY"'''
    _write_line(connection, "AI_GAME " + str(connectfour.columns(board)) + " " + str(connectfour.rows(board)))
    assert assert_ready(connection) == True
    
def assert_ready(connection):
    '''Ensures the next server response is "READY"'''
    response = _read_line(connection)
    if response == 'READY':
        return True
    else:
        raise I32CFSPProtocolError()
    
def provide_server_turn(connection: I32CFSPConnection, turn_move: list[str | list]) -> bool:
    '''Gives the server the client's connectfour move information. Returns True if the server
    respondes with "OKAY"'''
    _write_line(connection, str(turn_move[0]+" "+str(turn_move[1])))

    response = _read_line(connection)

    if response == 'OKAY':
        return True
    elif response.startswith('NO_USER '):
        return False
    else:
        raise I32CFSPProtocolError()

def read_server_move(connection: I32CFSPConnection, board: connectfour.GameState) -> connectfour.GameState:
    '''Interprets the connectfour move returned by the server into the client's GameState, and ensures that
    the next response from the server is one of three expected confirmations ("READY", "WINNER_YELLOW", "WINNER_RED")'''
    response = _read_line(connection)
    lmove = response.split()
    try:
        if lmove[0] == 'DROP':
            board = connectfour.drop(board, int(lmove[1])-1)
            _read_line(connection) == "READY" or _read_line(connection) == "WINNER_YELLOW" or (_read_line(connection) == "WINNER_RED")
            return board
        elif lmove[0] == 'POP':
            board = connectfour.pop(board, int(lmove[1])-1)
            _read_line(connection) == "READY" or _read_line(connection) == "WINNER_YELLOW" or (_read_line(connection) == "WINNER_RED")
            return board
    except:
        raise I32CFSPProtocolError()
    

def close(connection: I32CFSPConnection) -> None:
    'Closes the connection to the I32CFSP server'
    connection.input.close()
    connection.output.close()
    connection.socket.close()

def _read_line(connection: I32CFSPConnection) -> str:
    '''Reads a line of text sent from the server and returns it without
    a newline on the end of it
    '''
    line = connection.input.readline()[:-1]
    if _SHOW_DEBUG_TRACE:
        print('RCVD: ' + line)
        

    return line

def _write_line(connection: I32CFSPConnection, line: str) -> None:
    '''Writes a line of text to the server, including the appropriate
    newline sequence, and ensures that it is sent immediately.
    '''
    connection.output.write(line + '\r\n')
    connection.output.flush()

    if _SHOW_DEBUG_TRACE:
        print('SENT: ' + line)
