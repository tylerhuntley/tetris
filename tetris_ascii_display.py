from tetris_core import Game
from threading import Timer
from msvcrt import kbhit, getch
from time import time
import os

GAME = Game()
MOVES = {b'a': (-1, 0),
         b's': (0, -1),
         b'd': (1, 0)}

try:
    from msvcrt import kbhit, getch
except ImportError:
    def kbhit():
        import tty, termios
    def getch():
        pass


def main_threaded():
    """Handle timing of the forced moves, while allowing for input
    Why did I ever think this was a good idea?"""
    t = Timer(GAME.pace, main)
    t.start()
    if GAME.started:
        if GAME.can_move(0, -1):
            GAME.move_piece(0, -1)
            display()
        else:
            GAME.freeze_piece()
            GAME.clear_full_rows()
            if GAME.game_over():
                print('Game Over! Your score was:', GAME.score)
                t.cancel()
            else:
                GAME.load_next_piece()
                display()
    else:
        GAME.start()
        display()

    # Handle keyboard input
    while GAME.started:
        if kbhit():
            key = getch()
            if key in MOVES and GAME.can_move(*MOVES[key]):
                GAME.move_piece(*MOVES[key])
                display()
            elif key == b'w' and GAME.can_rotate():
                GAME.rotate_piece()
                display()

def main_timed():
    """Handle timing of the forced moves, while allowing for input"""
    GAME.start()
    display()
    last_force = time()
    while GAME.started:
        if last_force + GAME.pace < time():
            last_force = time()
            if GAME.can_move(0, -1):
                GAME.move_piece(0, -1)
                display()
            else:
                GAME.freeze_piece()
                GAME.clear_full_rows()
                if GAME.game_over():
                    print('Game Over! Your score was:', GAME.score)
                else:
                    GAME.load_next_piece()
                    display()

    # Handle keyboard input
        if kbhit():
            key = getch()
            if key in MOVES and GAME.can_move(*MOVES[key]):
                GAME.move_piece(*MOVES[key])
                display()
            elif key == b'w' and GAME.can_rotate():
                GAME.rotate_piece()
                display()

def main_ext():
    GAME.start()
    display()
    last_force = time()

    while not GAME.game_over():
        if last_force + GAME.pace < time():
            last_force = time()
            GAME.force_move()
            display()

        # Handle keyboard input
        if kbhit():
            key = getch()
            if key in MOVES and GAME.can_move(*MOVES[key]):
                GAME.move_piece(*MOVES[key])
                display()
            elif key == b'w' and GAME.can_rotate():
                GAME.rotate_piece()
                display()

    print('Game Over! Your score was:', GAME.score)


# T = Timer(GAME.pace, main)


# def reset_timer(f):
#     def g():
#         global T
#         try:
#             T.cancel()
#         except NameError:
#             pass
#         f()
#         # T = Timer(GAME.pace, main)
#         # T.start()
#     return g


# @reset_timer
def display():
    """Generate and print an ascii interface for the game"""
    screen = ''
    os.system('cls')
    for y in range(2, -2, -1):
        temp = '  '
        for x in range(-1, 2):
            temp += ('  ', '[]')[(x, y) in GAME.get_next_blocks()]
        screen += temp + '\n'
    screen += f"  -Next-{' '*(15-len(str(GAME.score)))}Score: {GAME.score}\n"
    screen += '~'*32 + '\n'
    for row in GAME.grid.rows[19::-1]:
        screen += '|'
        for node in row:
            screen += (' _ ', '[_]')[node.occupied or node.coords in GAME.get_active_blocks()]
        screen += '|\n'
    screen += '~'*32 + '\n'
    print(screen)


# main_timed()
main_ext()