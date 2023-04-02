import pygame
from pygame.sprite import Sprite
from random import randint


class Bird(Sprite):
    def __init__(self, screen_size, up_speed, down_speed, size, id, tube_group=None, use_ia=None):
        super().__init__()
        self.size = size
        self.up_speed = up_speed
        self.down_speed = down_speed
        
        imgs = ['bird_blue', 'bird_green', 'bird_purple', 'bird_red', 'bird_yellow']
        self.image = pygame.transform.scale(
            pygame.image.load(f'images/{imgs[id%len(imgs)]}.png'), tuple(self.size)
        )
        self.screen_size = screen_size
        self.x_start_pos = 90
        self.y_start_pos = randint(self.size.y, self.screen_size.y - self.size.y)
        self.rect = self.image.get_rect(center=(self.x_start_pos, self.y_start_pos))
        self.points = 0
        self.ia = self.create_ia() if use_ia else None
        self.tube_group = tube_group
        self.id = id

    def update(self, points):
        if self.ia:
            self.ia_action()
        else:
            self.human_action()

        if self.rect.y <= 0:
            self.rect.y = 0
        elif self.rect.y >= self.screen_size.y - self.size.y:
            self.rect.y = self.screen_size.y - self.size.y
        
        self.points = points

    def go_up(self):
        self.rect.y -= self.up_speed

    def go_down(self):
        self.rect.y += self.down_speed

    def create_ia(self):
        return True

    def ia_action(self):
        visible_tubes = [tube.rect.x for tube in self.tube_group.sprites() if tube.rect.x < self.screen_size.x and tube.rect.x > 0][0:4]

        if randint(0,10) < 8:
            self.go_up()
        else:
            self.go_down()

    def human_action(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.go_up()
        else:
            self.go_down()

    def lost_game(self):
        print(f'passaro {self.id} colidiu - pontuação {self.points}')
        self.kill()
