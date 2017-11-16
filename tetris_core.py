import random

WIDTH = 10
HEIGHT = 20

class Game():
    def __init__(self):
        self.grid = Grid(self)
        self.next_piece = pick_tetrad()
        self.current_piece = None
        self.started = False

    def pick_tetrad(self):
        return random.choice([L(self), J(self), O(self), I(self), S(self), Z(self), T(self)])

    def start(self):
        self.started = True
        self.next_block()

    def next_block(self):
        self.current_piece = self.next_piece
        self.next_piece = pick_tetrad()
        self.current_piece.move()

    def foo(self):
        pass


class Grid():
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


class Node():
    def __init__(self, grid, x, y):
        self.grid = grid
        self.occupied = False
        self.coords = (x, y)
        self.color = [0, 0, 0, 1]
        self.adjacent = [(1, 0), (0, 1), (-1, 0), (0, -1)]

    def occupy(self):
        self.occupied = True


class Block():
    def __init__(self, node):
        self.node = node
        self.move_to(*node.coords)

    def move_to(self, x, y):
        self.x = x
        self.y = y
        self.pos = (x, y)

    @property
    def coords(self):
        return self.x, self.y


class Tetrad():
    def __init__(self, game, shape=[]):
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
            blocks_xy.append(a + b for a, b in zip(self.center_xy, block))
        return blocks_xy        
    
    def rotate(self):
        for i, b in enumerate(self.blocks):
            self.blocks[i] = self.rotated[n]

    def move_rel(self, vector):
        self.center_xy = (a + b for a, b in zip(vector, self.center_xy))

    def move_abs(self, to):
        self.center_xy = to

    def move(self):
        if any([self.game.grid.node(*node).occupied for node in self.get_blocks_xy()]):
            self.freeze()
        else:
            self.move_rel((0, -1))

    def freeze(self):
        for node in self.get_blocks_xy():
            self.game.grid.node(*node).occupy()



class L(Tetrad):
    def __init__(self):
        super().__init__(shape=[(0, 1), (0, 0), (0, -1), (1, -1)])

class J(Tetrad):
    def __init__(self):
        super().__init__(shape=[(0, 1), (0, 0), (0, -1), (-1, -1)])

class O(Tetrad):
    def __init__(self):
        super().__init__(shape=[(0, 0), (0, -1), (-1, -1), (-1, 0)])

class I(Tetrad):
    def __init__(self):
        super().__init__(shape=[(0, 1), (0, 0), (0, -1), (0, -2)])

class S(Tetrad):
    def __init__(self):
        super().__init__(shape=[(1, 0), (0, 0), (0, -1), (-1, -1)])

class Z(Tetrad):
    def __init__(self):
        super().__init__(shape=[(-1, 0), (0, 0), (0, -1), (1, -1)])

class T(Tetrad):
    def __init__(self):
        super().__init__(shape=[(0, 0), (0, -1), (-1, 0), (0, 1)])