from collections import namedtuple
from random import randint

import pygame
from pygame.sprite import Sprite

Point = namedtuple('Point', ['x', 'y'])


class Tube(Sprite):
    def __init__(
        self,
        tube_type,
        speed,
        screen_size,
        other_tube,
        previous_tube,
        bird_space,
        previous_tube_distance,
    ):
        super().__init__()
        self.tube_type = tube_type
        self.speed = speed
        self.image = self.__define_image()

        self.bird_space = bird_space
        self.previous_tube_distance = previous_tube_distance

        self.img_size = Point(*self.image.get_size())
        self.screen_size = Point(*screen_size)
        self.img_center = Point(x=self.img_size.x / 2, y=self.img_size.y / 2)
        self.tube_size = Point(*self.__define_tube_size(other_tube))
        self.rect = self.image.get_rect(
            center=self.__define_center(previous_tube)
        )

    def __define_tube_size(self, other_tube):
        if not other_tube:
            max_size_ = self.screen_size.y - self.bird_space
            max_size = (
                max_size_ if max_size_ < self.img_size.y else self.img_size.y
            )
            return (self.img_size.x, randint(50, max_size))
        else:
            tube_size = (
                self.screen_size.y - other_tube.tube_size.y - self.bird_space
            )
            return (self.img_size.x, tube_size)

    def __define_center(self, previous_tube):
        if self.tube_type == 'bottom':
            y = self.screen_size.y - (self.tube_size.y - self.img_center.y)
        else:
            y = self.tube_size.y - self.img_center.y

        if previous_tube:
            x = previous_tube.rect.x + self.previous_tube_distance
        else:
            x = self.screen_size.x

        return (x, y)

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
