#!/usr/bin/python

import pygame
import blocks
from board import Board
from Queue import Queue
from processes import Updater,EventListener
from utils import *
import threading

CELL_SIZE=8
BOARD_WIDTH=10
BOARD_HEIGHT=40

CONTAINER_COLOUR=(255,255,255)


class Tetris():

    def __init__(self):
        self.queue = Queue()
        self.updater = Updater(self.queue)
        self.event_listener = EventListener(self.queue)
        updater_thread = threading.Thread(target = self.updater.run)
        event_listener_thread = threading.Thread(target=self.event_listener.run)
        updater_thread.start()
        event_listener_thread.start()
        pygame.init()
        self.surf = pygame.display.set_mode((640,400))
        self.board = Board(self.surf,(BOARD_WIDTH,BOARD_HEIGHT),CELL_SIZE, (280,40))
        self.block = blocks.new_block((BOARD_WIDTH/2,1))
        self.draw_container()
        pygame.display.update()
        self.running = False

    def draw_container(self):
        pygame.draw.lines(self.surf,CONTAINER_COLOUR, False, [(279,40),(279,360),(361,360),(361,40)])

    def quit(self):
        print 'Quitting'
        self.running = False

    def update(self):
        if not(self.move_block(DOWN)):
            self.updater.delay = 0.5
            self.board.draw(self.block.get_cells(), self.block.get_colour(), True)
            self.board.check_lines()
            self.block = blocks.new_block((BOARD_WIDTH/2,1))

    def process(self):
        command = self.queue.get()
        if command == 'UPDATE':
            self.update()
        if command == 'QUIT':
            self.quit()
        if command=='MOVERIGHT':
            self.move_block(RIGHT)
        if command == 'MOVELEFT':
            self.move_block(LEFT)
        if command == 'ROTATE':
            self.rotate()
        if command=='DROP':
            self.updater.delay = 0

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
            self.process()
            pygame.display.update()
        pygame.quit()

if __name__ == "__main__":
    app = Tetris()
    app.run()