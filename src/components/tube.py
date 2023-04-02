import pygame
from pygame.sprite import Sprite


class Tube(Sprite):
    def __init__(
        self,
        tube_type,
        speed
    ):
        super().__init__()
        self.tube_type = tube_type
        self.speed = speed
        self.image = self.__define_image()
        self.size = None

    def define_position(self, x, y):
        self.rect = self.image.get_rect(center=(x, y))

    def __define_image(self):
        if self.tube_type == 'bottom':
            return pygame.image.load('images/tube.png')
        elif self.tube_type == 'top':
            return pygame.transform.rotate(
                pygame.image.load('images/tube.png'), 180
            )

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.image.get_size()[0]:
            self.kill()
