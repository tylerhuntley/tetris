import random
from threading import Timer

WIDTH = 10
HEIGHT = 20


class Game:
    def __init__(self):
        self.grid = Grid(self)
        self.next_piece = self.pick_tetrad()
        self.current_piece = None
        self.started = False

    def pick_tetrad(self):
        return random.choice([L(self), J(self), O(self), I(self), S(self), Z(self), T(self)])

    def start(self):
        self.started = True
        self.next_block()
        self.main_loop()

    def next_block(self):
        self.current_piece = self.next_piece
        self.next_piece = self.pick_tetrad()
        self.current_piece.move_abs(5, 20)

    def main_loop(self):
        if self.current_piece.move_down():
            t = Timer(1.0, self.main_loop())
            t.start()
        elif any([node.occupied for node in self.grid.rows[20]]):
            self.game_over()
        else:
            self.next_piece()
            t = Timer(1.0, self.main_loop())
            t.start()

    def game_over(self):
        self.started = False


class Grid:
    def __init__(self, game):
        self.game = game
        self.rows = []
        for y in range(20):
            row = []
            for x in range(10):
                row.append(Node(self, x, y))
            self.rows.append(row)

    def node(self, x, y):
        return self.rows[y][x]

    def get_full_rows(self):
        full_rows = []
        for row in self.rows:
            if all([node.occupied for node in row]):
                full_rows.append(row)
        return full_rows

    @staticmethod
    def clear_row(row):
        for node in row:
            node.clear()


class Node:
    def __init__(self, grid, x, y):
        self.grid = grid
        self.occupied = False
        self.coords = (x, y)
        self.color = [0, 0, 0, 1]
        self.adjacent = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def occupy(self, block):
        self.occupied = True
        self.color = block.color

    def clear(self):
        self.occupied = False
        self.color = [0, 0, 0, 1]


# class Block:
#     def __init__(self, node):
#         self.node = node
#         self.move_to(*node.coords)
#
#     def move_to(self, x, y):
#         self.x = x
#         self.y = y
#         self.pos = (x, y)
#
#     @property
#     def coords(self):
#         return self.x, self.y


class Tetrad:
    def __init__(self, game, shape=[(0, 0)]):
        self.color = [1, 0, 0, 1]
        self.game = game
        self.center_xy = (0, 0)
        self.blocks = shape
        # Should probably use sin and cos and shit for this
        self.rotated = {(0, 1): (1, 0), (1, 0): (0, -1), (0, -1): (-1, 0), (-1, 0): (0, 1), 
                        (1, 1): (1, -1), (1, -1): (-1, -1), (-1, -1): (-1, 1), (-1, 1): (1, 1), 
                        (0, 2): (2, 0), (2, 0): (0, -2), (0, -2): (-2, 0), (-2, 0): (0, 2),
                        (0, 0): (0, 0)}
    
    def get_blocks_xy(self):
        """Return list of absolute coordinates of all contained blocks"""
        blocks_xy = []
        for block in self.blocks:
            blocks_xy.append(self.block_xy(block))
        return blocks_xy

    def block_xy(self, block):
        block_xy = (a + b for a, b in zip(self.center_xy, block))
        return block_xy
    
    def rotate(self):
        """Rotate all blocks around center_xy if possible, else do nothing"""
        new_blocks = []
        for block in self.blocks:
            if (self.block_xy(self.rotated[block])[0] in range(WIDTH) and
                self.block_xy(self.rotated[block])[1] > 0):
                new_blocks = self.rotated[block]
            else:
                break
        else:
            self.blocks = new_blocks

    def move_rel(self, x, y):
        self.center_xy = (a + b for a, b in zip((x, y), self.center_xy))

    def move_abs(self, x, y):
        self.center_xy = (x, y)

    def move_down(self):
        nodes = [self.game.grid.node(*block) for block in self.get_blocks_xy()]
        if any([node.occupied for node in nodes]) or
            any([node.coords[1] < 0 for node in nodes]):
            self.freeze()
            return False
        else:
            self.move_rel(0, -1)
            return True

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
        super().__init__(*args, shape=[(0, 1), (0, 0), (0, -1), (0, -2)])


class S(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(1, 0), (0, 0), (0, -1), (-1, -1)])


class Z(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(-1, 0), (0, 0), (0, -1), (1, -1)])


class T(Tetrad):
    def __init__(self, *args):
        super().__init__(*args, shape=[(0, 0), (0, -1), (-1, 0), (0, 1)])
