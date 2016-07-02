#!/usr/bin/python

import pygame
import blocks
from board_tft import BoardTFT as Board
from utils import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import Adafruit_ILI9341 as TFT
import Adafruit_GPIO.SPI as SPI

DC = 18
RST = 23
SPI_PORT = 0
SPI_DEVICE = 0

CELL_SIZE=7
BOARD_WIDTH=10
BOARD_HEIGHT=40

SCREEN_WIDTH=240
SCREEN_HEIGHT=320

MARGIN_X=(SCREEN_WIDTH-(CELL_SIZE*BOARD_WIDTH))/2
MARGIN_Y=(SCREEN_HEIGHT-(CELL_SIZE*BOARD_HEIGHT))/2

CONTAINER_COLOUR=(255,255,255)
REFRESH_PERIOD=150


class Tetris():

    def __init__(self):
        pygame.init()
        self.disp = TFT.ILI9341(DC, rst=RST, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE, max_speed_hz=64000000))
        self.disp.begin()
        self.disp.clear()
        self.draw = self.disp.draw()
        self.board = Board(self.draw,(BOARD_WIDTH,BOARD_HEIGHT),CELL_SIZE, (MARGIN_X,MARGIN_Y))
        self.block = blocks.new_block((BOARD_WIDTH/2,1))
        self.display_next_block()
        self.draw_container()
        self.last_update=timestamp()
        self.update_delay = REFRESH_PERIOD
        self.score = 0
        self.update_score(0)
        self.disp.display()
        self.running = False

    def draw_container(self):
        self.draw.line((MARGIN_X-1, MARGIN_Y, MARGIN_X-1, MARGIN_Y+(CELL_SIZE*BOARD_HEIGHT)+1), fill=CONTAINER_COLOUR)
        self.draw.line((MARGIN_X-1, MARGIN_Y+(CELL_SIZE*BOARD_HEIGHT)+1,MARGIN_X+(CELL_SIZE*BOARD_WIDTH) + 1, MARGIN_Y+(CELL_SIZE*BOARD_HEIGHT)+1), fill=CONTAINER_COLOUR)
        self.draw.line((MARGIN_X+(CELL_SIZE*BOARD_WIDTH) + 1, MARGIN_Y+(CELL_SIZE*BOARD_HEIGHT)+1, MARGIN_X+(CELL_SIZE*BOARD_WIDTH) + 1, MARGIN_Y), fill=CONTAINER_COLOUR)

    def quit(self):
        print 'Quitting'
        self.running = False

    def update(self):
        if not(self.move_block(DOWN)):
            self.new_block()

    def display_next_block(self):
        next_block = blocks.get_next_block_display()
        self.board.display_next_block(next_block.get_cells(), next_block.get_colour(), (180,60))

    def new_block(self):
        if self.block.pos[1]<2:
            self.game_over()
        self.update_delay = REFRESH_PERIOD
        self.board.draw_cells(self.block.get_cells(), self.block.get_colour(), True)
        lines_cleared = self.board.check_lines()
        self.update_score(10+{0: 0, 1: 100, 2: 250, 3: 500, 4: 1000}.get(lines_cleared))
        self.block = blocks.new_block((BOARD_WIDTH / 2, 1))
        self.display_next_block()

    def game_over(self):
        print "Final Score: %s" % self.score
        self.quit()

    def update_score(self, delta):
        self.score += delta
        self.board.display_score(self.score)

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
            self.board.draw_cells(self.block.get_cells(), (0, 0, 0))
            self.block.rotate()
            self.board.draw_cells(self.block.get_cells(), self.block.get_colour())

    def move_block(self, direction):
        new_cells = self.block.get_new_cells(direction)
        if self.board.can_place(new_cells):
            self.board.draw_cells(self.block.get_cells(), (0, 0, 0))
            self.block.move(direction)
            self.board.draw_cells(self.block.get_cells(), self.block.get_colour())
            return True
        return False

    def run(self):
        self.running = True
        while self.running:
            #self.handle_events()
            self.check_update()
            self.disp.display()
        pygame.quit()

if __name__ == "__main__":
    app = Tetris()
    app.run()