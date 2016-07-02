#!/usr/bin/python
import pygame
from pygame.locals import *

from math import *


BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
DARKGRAY = (40, 40, 40)


class App:
    def __init__(self):
        self._running = True
        self._display_surf = None
        self.size = self.weight, self.height = 640, 400
        self.cx, self.cy = 128,128
        self.t=0.0

    def on_init(self):
        pygame.init()
        self._display_surf = pygame.display.set_mode(self.size)
        pygame.display.set_caption('Hello World')
        self._running = True

    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_render(self):
        for x in range(256):
            for y in range(256):
                self._display_surf.set_at((x + 192, y + 72), self.get_colour((x/128.0), (y/128.0), self.t))

    def on_cleanup(self):
        pygame.quit()

    def on_execute(self):
        if self.on_init() == False:
            self._running = False

        while (self._running):
            for event in pygame.event.get():
                self.on_event(event)
            self.t+=0.01
            self.on_render()
            pygame.display.update()
        self.on_cleanup()


    def get_colour(self,x,y,t):
        v = sin(x*2.0+t)
        v += cos(y * 2.0 + t)
        v += sin(0.05*(x*sin(t/4)+y*cos(t/6)))
        cx = x + 0.5*sin(t*10.0)
        cy = y + 0.5-cos(t*8.0)
        v += sin(10.0*sqrt(cx*cx+cy*cy+1)+t)/2.0
        r,g,b = (cos(v*3.0),sin(v*3.0),sin(v*2.0))
        return (self.col_smooth(r),self.col_smooth(g),self.col_smooth(b))


    def col_smooth(self, d):
        n = d*256+256
        if n>256:
            n = 512 - n
        return n % 256


if __name__ == "__main__":
    theApp = App()
    theApp.on_execute()