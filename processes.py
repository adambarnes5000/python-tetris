import time
import pygame


class Updater():

    def __init__(self, queue, delay=0.5):
        self.queue = queue
        self.delay = delay
        self.running = True

    def run(self):
        while self.running:
            self.queue.put('UPDATE')
            time.sleep(self.delay)


class EventListener():
    def __init__(self, queue):
        self.queue = queue
        self.running = True

    def run(self):
        time.sleep(1.5)
        while self.running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        self.queue.put('MOVELEFT')
                    if event.key == pygame.K_RIGHT:
                        self.queue.put('MOVERIGHT')
                    if event.key == pygame.K_DOWN:
                        self.queue.put('DROP')
                    if event.key == pygame.K_RETURN or event.key == pygame.K_UP:
                        self.queue.put('ROTATE')
                if event.type == pygame.QUIT:
                    self.queue.put('QUIT')