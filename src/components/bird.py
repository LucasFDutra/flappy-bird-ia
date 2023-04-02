import pygame
from pygame.sprite import Sprite


class Bird(Sprite):
    def __init__(self, screen_size, up_speed, down_speed, size):
        super().__init__()
        self.size = size
        self.up_speed = up_speed
        self.down_speed = down_speed
        self.image = pygame.transform.scale(
            pygame.image.load('images/bird.png'), tuple(self.size)
        )
        self.screen_size = screen_size
        self.rect = self.image.get_rect(center=(90, self.screen_size.y / 2))
        self.points = 0

    def update(self, points, go_up=False):
        keys = pygame.key.get_pressed()
        y_ = self.rect.y
        if keys[pygame.K_SPACE] or go_up:
            self.rect.y -= self.up_speed
        else:
            self.rect.y += self.down_speed

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= self.screen_size.y - self.size.y:
            self.rect.y = self.screen_size.y - self.size.y
        
        self.points = points
