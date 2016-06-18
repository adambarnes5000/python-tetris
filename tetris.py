#!/usr/bin/python

import pygame
import blocks
from board import Board
from utils import *

CELL_SIZE=8
BOARD_WIDTH=10
BOARD_HEIGHT=40

CONTAINER_COLOUR=(255,255,255)
REFRESH_PERIOD=250

class Tetris():

    def __init__(self):
        pygame.init()
        self.surf = pygame.display.set_mode((640,400))
        self.board = Board(self.surf,(BOARD_WIDTH,BOARD_HEIGHT),CELL_SIZE, (280,40))
        self.block = blocks.new_block((BOARD_WIDTH/2,1))
        self.update_next_block()
        self.draw_container()
        self.last_update=timestamp()
        self.update_delay = REFRESH_PERIOD
        self.score = 0
        self.update_score(0)
        pygame.display.update()
        self.running = False

    def draw_container(self):
        pygame.draw.lines(self.surf,CONTAINER_COLOUR, False, [(279,40),(279,360),(361,360),(361,40)])

    def quit(self):
        print 'Quitting'
        self.running = False

    def update(self):
        if not(self.move_block(DOWN)):
            self.new_block()

    def display_next_block(self):
        next_block = blocks.get_next_block_display()
        self.board.display_next_block(next_block.get_cells(), next_block.get_colour())

    def new_block(self):
        if self.block.pos[1]<2:
            self.game_over()
        self.update_delay = REFRESH_PERIOD
        self.board.draw(self.block.get_cells(), self.block.get_colour(), True)
        lines_cleared = self.board.check_lines()
        self.update_score(10+{0: 0, 1: 100, 2: 250, 3: 500, 4: 1000}.get(lines_cleared))
        self.block = blocks.new_block((BOARD_WIDTH / 2, 1))
        self.update_next_block()

    def game_over(self):
        print "Final Score: %s" % self.score
        self.quit()

    def update_score(self, delta):
        self.score += delta
        self.board.display_score(self.score)

    def update_next_block(self):
        next_block = blocks.get_next_block_display()
        self.board.display_next_block(next_block.get_cells(), next_block.get_colour())

    def check_update(self):
        if timestamp()-self.last_update > self.update_delay:
            self.last_update = timestamp()
            self.update()

    def handle_events(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.move_block(LEFT)
                if event.key == pygame.K_RIGHT:
                    self.move_block(RIGHT)
                if event.key == pygame.K_DOWN:
                    self.update_score(10*(40-self.block.pos[1]))
                    self.update_delay = 0
                if event.key == pygame.K_RETURN or event.key == pygame.K_UP:
                    self.rotate()
            if event.type == pygame.QUIT:
                self.quit()

    def rotate(self):
        new_cells = self.block.get_rotated_new_cells()
        if self.board.can_place(new_cells):
            self.board.draw(self.block.get_cells(), (0, 0, 0))
            self.block.rotate()
            self.board.draw(self.block.get_cells(), self.block.get_colour())

    def move_block(self, direction):
        new_cells = self.block.get_new_cells(direction)
        if self.board.can_place(new_cells):
            self.board.draw(self.block.get_cells(), (0, 0, 0))
            self.block.move(direction)
            self.board.draw(self.block.get_cells(), self.block.get_colour())
            return True
        return False

    def run(self):
        self.running = True
        while self.running:
            self.handle_events()
            self.check_update()
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    app = Tetris()
    app.run()