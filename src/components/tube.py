from pygame.sprite import Sprite
import pygame
from random import randint


class Tube(Sprite):
    def __init__(self, is_top, screen_size, other_tube, last_tube):
        super().__init__()
        if is_top:
            self.image = pygame.transform.rotate(pygame.image.load('images/tube.png'), 180)
        else:
            self.image = pygame.image.load('images/tube.png')

        img_size_x, img_size_y = self.image.get_size()
        screen_size_y = screen_size[1]
        if not other_tube:
            max_size = screen_size_y*0.7 if screen_size_y*0.7 < img_size_y else img_size_y
            tube_size_y = randint(50, max_size)

            tube_center = img_size_y/2
            y = screen_size_y - (tube_size_y - tube_center)
        else:
            tube_size_y = screen_size_y - other_tube.tube_size_y - 150
            tube_center = img_size_y/2
            y = (tube_size_y - tube_center)

        self.tube_size_y = tube_size_y
        if last_tube:
            x = last_tube.rect.x + 600
        else:
            x = screen_size[0]

        self.rect = self.image.get_rect(center = (x,y))

    def update(self):
        self.rect.x -= 2
        if self.rect.x < -self.image.get_size()[0]:
            self.kill()