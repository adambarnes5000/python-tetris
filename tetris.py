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
        self.draw_container()
        pygame.display.update()
        self.last_update=timestamp()
        self.update_delay = REFRESH_PERIOD
        self.running = False


    def draw_container(self):
        pygame.draw.lines(self.surf,CONTAINER_COLOUR, False, [(279,40),(279,360),(361,360),(361,40)])

    def quit(self):
        print 'Quitting'
        self.running = False

    def update(self):
        if not(self.move_block(DOWN)):
            self.update_delay = REFRESH_PERIOD
            self.board.draw(self.block.get_cells(), self.block.get_colour(), True)
            self.board.check_lines()
            self.block = blocks.new_block((BOARD_WIDTH/2,1))

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