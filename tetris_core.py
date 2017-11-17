import random

WIDTH = 10
HEIGHT = 20


class Game:
    def __init__(self):
        self.grid = Grid(self)
        self.next_piece = self.choose_new_piece()
        self.current_piece = None
        self.started = False
        self.score = 0

    @property
    def pace(self):
        """To handle speed progression..."""
        return 1.0

    # def main_loop(self):
    #     t = Timer(self.pace, self.main_loop)
    #     t.start()
    #     if not self.started:
    #         self.start()
    #
    #     if self.can_move(0, -1):
    #         self.move_piece(0, -1)
    #     else:
    #         self.freeze_piece()
    #         self.clear_full_rows()
    #         if self.game_over():
    #             t.cancel()
    #         else:
    #             self.load_next_piece()
    #
    #     # Handle keyboard input
    #     while self.started:
    #         if kbhit():
    #             key = getch()
    #             if key in MOVES and self.can_move(*MOVES[key]):
    #                 self.move_piece(*MOVES[key])
    #             elif key == b'w' and self.can_rotate():
    #                 self.rotate_piece()

    def choose_new_piece(self):
        tetrad = random.choice([L, J, O, I, S, Z, T])
        return tetrad(self)
        # return random.choice([L(self), J(self), O(self), I(self), S(self), Z(self), T(self)])

    def get_active_blocks(self):
        return self.current_piece.get_blocks_xy()

    def get_next_blocks(self):
        return self.next_piece.get_blocks_xy()

    def start(self):
        self.started = True
        return self.load_next_piece()

    def load_next_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = self.choose_new_piece()
        self.current_piece.move_abs(WIDTH//2, HEIGHT)
        self.grid.load_piece(self.current_piece)

    def can_move(self, x, y):
        for block in self.current_piece.get_moved_xy((x, y)):
            if block[0] not in range(WIDTH) or block[1] < 0 or self.grid.node(*block).occupied:
                return False
        return True

    def can_rotate(self):
        for block in self.current_piece.get_rotated_xy():
            if block[0] not in range(WIDTH) or self.grid.node(*block).occupied:
                return False
        return True

    def move_piece(self, x, y):
        for coord in self.current_piece.get_moved_xy((x, y)):
            if self.grid.node(*coord).occupied:
                break
        else:
            self.current_piece.move_rel(x, y)
            if y == -1:
                self.score += 4

    def rotate_piece(self):
        for coord in self.current_piece.get_rotated_xy():
            if self.grid.node(*coord).occupied:
                break
        else:
            self.current_piece.rotate()

    def freeze_piece(self):
        for block in self.current_piece.get_blocks_xy():
            self.grid.node(*block).occupy(self.current_piece)

    def clear_full_rows(self):
        rows = self.grid.get_full_rows()
        for row in rows:
            self.grid.clear_row(row)
            self.score += 10
        self.drop_floating_blocks(rows)

    def drop_floating_blocks(self, rows):
        """Lower floating blocks in every row above every empty row"""
        for row in rows:
            rows_to_drop = (self.grid.rows[i] for i in range(row, HEIGHT))
            for row_to_drop in rows_to_drop:
                for node in row_to_drop:
                    if node.occupied:
                        node.clear()
                        self.grid.node(*vector_add(node.coords, (0, -1))).occupy(node.color)

    def game_over(self):
        if any([node.occupied for node in self.grid.rows[HEIGHT-1]]):
            self.started = False
            return True


class Grid:
    def __init__(self, game):
        self.game = game
        self.active_piece = None
        self.rows = []
        for y in range(HEIGHT+2):
            row = []
            for x in range(WIDTH):
                row.append(Node(self, x, y))
            self.rows.append(row)

    def node(self, x=None, y=None):
        try:
            return self.rows[y][x]
        except TypeError:
            return Node(self, -1, -1)

    def load_piece(self, piece):
        self.active_piece = piece

    def freeze_piece(self):
        for block in self.active_piece.get_blocks_xy():
            self.node(*block).occupy(block)

    def get_full_rows(self):
        """Return list of indices of every fully occupied row"""
        full_rows = []
        for i, row in enumerate(self.rows):
            if all([node.occupied for node in row]):
                full_rows.append(i)
        return full_rows

    def clear_row(self, row):
        for node in self.rows[row]:
            node.clear()
        return row


class Node:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.occupied = False
        self.coords = (x, y)
        self.color = [0, 0, 0, 1]

    def occupy(self, color=(1, 1, 1, 1)):
        self.occupied = True
        self.color = color

    def clear(self):
        self.occupied = False
        self.color = [0, 0, 0, 1]


def vector_add(x, y):
    return tuple(a + b for a, b in zip(x, y))


def rotate(tup):
    (x, y) = tup
    return y, -x


class Tetrad:
    def __init__(self, game, shape=None, *args):
        self.color = [1, 0, 0, 1]
        self.game = game
        self.center_xy = (0, 0)
        self.blocks = shape

        # self.rotated = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1),
        #                 (1, 1): (1, -1), (1, -1): (-1, -1), (-1, -1): (-1, 1), (-1, 1): (1, 1),
        #                 (0, 2): (2, 0), (2, 0): (0, -2), (0, -2): (-2, 0), (-2, 0): (0, 2),
        #                 (0, 0): (0, 0)}

    def get_block_xy(self, block):
        """Return absolute coordinates from given block's relative coordinates"""
        return vector_add(self.center_xy, block)

    def get_blocks_xy(self):
        """Return list of absolute coordinates of all contained blocks"""
        return [self.get_block_xy(block) for block in self.blocks]

    def get_moved_xy(self, vector):
        """Return list of absolute coordinates off all blocks shifted by vector"""
        return list(vector_add(block, vector) for block in self.get_blocks_xy())

    def get_rotated_xy(self):
        """Return list of absolute coordinates of all blocks rotated around center_xy"""
        return list(self.get_block_xy(block) for block in (rotate(block) for block in self.blocks))

    def move_rel(self, x, y):
        """Shift absolute center coordinates by (x, y)"""
        self.center_xy = vector_add(self.center_xy, (x, y))

    def move_abs(self, x, y):
        self.center_xy = (x, y)

    def rotate(self):
        """Pivot all blocks around center"""
        self.blocks = list(rotate(block) for block in self.blocks)

    def freeze(self):
        for block in self.get_blocks_xy():
            self.game.grid.node(*block).occupy(self)


class L(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, 1), (0, 0), (0, -1), (1, -1)])


class J(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, 1), (0, 0), (0, -1), (-1, -1)])


class O(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, 0), (0, -1), (-1, -1), (-1, 0)])


class I(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, -1), (0, 0), (0, 1), (0, 2)])


class S(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(1, 0), (0, 0), (0, -1), (-1, -1)])


class Z(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(-1, 0), (0, 0), (0, -1), (1, -1)])


class T(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, 0), (0, -1), (-1, 0), (0, 1)])
