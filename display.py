#!/usr/bin/python
import pygame
from pygame.locals import *

import math


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.cx, self.cy = 128,128

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Hello World')
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def get_colour(self,x,y):
        d = math.sqrt(((self.cx-x)*(self.cx-x))+((self.cy-y)*(self.cy-y)))
        return (x%256,y%256,d%256)

    def on_loop(self):
        self.cx = (self.cx+10)%256

    def on_render(self):
        for x in range(256):
            for y in range(256):
                self._display_surf.set_at((x + 192, y + 72), self.get_colour(x, y))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()
            pygame.display.update()
        self.on_cleanup()


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()