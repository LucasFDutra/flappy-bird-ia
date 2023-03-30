import pygame
from pygame.sprite import Sprite


class Bird(Sprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('images/bird.png'), (25, 25)
        )
        self.screen_size = screen_size
        self.rect = self.image.get_rect(center=(90, self.screen_size[1] / 2))

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= 5
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= self.screen_size[1] - 25:
            self.rect.y = self.screen_size[1] - 25
        else:
            self.rect.y += 3
