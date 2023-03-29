from pygame.sprite import Sprite
import pygame

class Bird(Sprite):
    def __init__(self, screen_size):
        super().__init__()
        self.image = pygame.transform.scale(
            pygame.image.load('images/bird.png'),
            (25,25)
        )
        self.rect = self.image.get_rect(center=(90, screen_size[1]/2))

    def update(self, lost_function, points):
        self.rect.y += 3
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.rect.y -= 5
        if self.rect.y <= 0:
            self.rect.y = 0
        if self.rect.y >= 540:
            lost_function(points)