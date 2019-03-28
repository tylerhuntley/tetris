from tetris_core import Game
from time import time
import os

GAME = Game()
MOVES = {'a': (-1, 0),
         's': (0, -1),
         'd': (1, 0)}

# Handle terminal interactions on Windows
try:
    from msvcrt import kbhit, getch
    def clear():
        os.system('cls')

# Handle terminal interactions on Mac/Linux
except ImportError:
    import sys, termios, atexit
    from select import select

    # Save normal terminal settings
    fd = sys.stdin.fileno()
    old_term = termios.tcgetattr(fd)

    def set_normal_term():
        termios.tcsetattr(fd, termios.TCSAFLUSH, old_term)

    # Debuffer new terminal until exit
    new_term = termios.tcgetattr(fd)
    new_term[3] = (new_term[3] & ~termios.ICANON & ~termios.ECHO)

    def set_curses_term():
        termios.tcsetattr(fd, termios.TCSAFLUSH, new_term)

    atexit.register(set_normal_term)
    set_curses_term()

    def kbhit():
        dr,dw,de = select([sys.stdin], [], [], 0)
        return dr != []

    def getch():
        return sys.stdin.read(1)

    def clear():
        os.system('clear')


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
            elif key == 'w' and GAME.can_rotate():
                GAME.rotate_piece()
                display()

    print('Game Over! Your score was:', GAME.score)


def display():
    """Generate and print an ascii interface for the game"""
    screen = ''
    clear()
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


if __name__ == '__main__':
    main_ext()
