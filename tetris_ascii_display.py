from tetris_core import Game
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


if __name__ == '__main__':
	main_ext()