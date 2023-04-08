import pygame
from pygame.sprite import Sprite
from random import randint
from uuid import uuid4


class Bird(Sprite):
    def __init__(self, size, speed, gravity, x, y):
        super().__init__()
        self.size = size
        self.speed = speed
        self.gravity = gravity
        self.id = str(uuid4())
        self.points = 0
        self.time = 0
        
        img = ['bird_blue', 'bird_green', 'bird_purple', 'bird_red', 'bird_yellow'][randint(0,4)]
        self.image = pygame.transform.scale(
            pygame.image.load(f'images/{img}.png'), tuple(self.size)
        )
        self.rect = self.image.get_rect(center=(x, y))

    def update(self, points):
        self.time += 1
        if self.rect.y <= 0: self.rect.y = 0
        if self.rect.y + self.size.y >= 600: self.rect.y = 600 - self.size.y
        
        self.points = points

    def go_up(self):
        self.rect.y -= self.deslocamento()
        self.time = 0
        #print('subindo')

    def go_down(self):
        self.rect.y += self.deslocamento()
        #print('descendo')

    def deslocamento(self):
        s = (self.speed*self.time) + ((self.gravity*(self.time**2))/2)
        return s if s <= 16 else 16
