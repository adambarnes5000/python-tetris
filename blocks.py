import random
from utils import *

BLOCKS = (
    ((((-1,-1),(0,-1),(0,0),(1,0)),((1,-1),(0,0),(1,0),(0,1)),((-1,0),(0,0),(0,1),(1,1)),((-1,-1),(-1,0),(0,0),(0,1))), (200,50,50)),
    ((((0,-1),(1,-1),(-1,0),(0,0)),((0,-1),(0,0),(1,0),(1,1)),((0,0),(1,0),(-1,1),(0,1)),((-1,-1),(-1,0),(0,0),(0,1))),(50,50,200)),
    ((((0,-1),(-1,0),(0,0),(1,0)),((0,-1),(0,0),(1,0),(0,1)),((-1,0),(0,0),(1,0),(0,1)),((0,-1),(-1,0),(0,0),(0,1))),(50,200,50)),
    ((((0,-1),(0,0),(0,1),(1,1)),((-1,0),(0,0),(1,0),(-1,1)),((-1,-1),(0,-1),(0,0),(0,1)),((1,-1),(-1,0),(0,0),(1,0))),(200,200,50)),
    ((((0,-1),(0,0),(-1,1),(0,1)),((-1,-1),(-1,0),(0,0),(1,0)),((0,-1),(1,-1),(0,0),(0,1)),((-1,0),(0,0),(1,0),(1,1))),(200,50,200)),
    ((((0,-1),(1,-1),(0,0),(1,0)),((0,-1),(1,-1),(0,0),(1,0)),((0,-1),(1,-1),(0,0),(1,0)),((0,-1),(1,-1),(0,0),(1,0))),(50,200,200)),
    ((((0,-1),(0,0),(0,1),(0,2)),((-1,0),(0,0),(1,0),(2,0)),((0,-1),(0,0),(0,1),(0,2)),((-1,0),(0,0),(1,0),(2,0))),(200,200,200))
    )

next_block = random.choice(BLOCKS)


class Block():

    def __init__(self, block_data, pos):
        self.data = block_data
        self.rotation = 0
        self.pos = pos

    def get_cells(self):
        return map(lambda c: add_tuples(self.pos, c), self.data[0][self.rotation])

    def get_colour(self):
        return self.data[1]

    def move(self, direction):
        self.pos = add_tuples(self.pos, direction)

    def rotate(self):
        self.rotation = (self.rotation + 1) % 4

    def get_rotated_new_cells(self):
        new_rotation = (self.rotation + 1) % 4
        return map(lambda c: add_tuples(self.pos, c), self.data[0][new_rotation])

    def get_new_cells(self, direction):
        return map(lambda c: add_tuples(add_tuples(self.pos, c),direction), self.data[0][self.rotation])


def get_next_block_display():
    return Block(next_block, (0,0))


def new_block(position):
    global next_block
    block = Block(next_block, position)
    next_block = random.choice(BLOCKS)
    return block