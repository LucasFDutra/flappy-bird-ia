from random import randint

import pygame
from src.utils import Point
from src.components import Bird, Tube


class Game():
    def __init__(self, collide) -> None:
        pygame.init()

        self.screen_size = Point(x=800, y=600)
        
        self.surface = pygame.display.set_mode(size=tuple(self.screen_size))
        self.clock = pygame.time.Clock()

        self.font_end = pygame.font.SysFont('arial', 50)
        self.font_score = pygame.font.SysFont('arial', 10)
        
        self.tube_group = pygame.sprite.Group()
        self.bottom_tube_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()

        self.background = pygame.transform.scale(
            pygame.image.load('images/background.png'), size=tuple(self.screen_size)
        )
        
        self.points = 0
        self.fps = 30
        self.gravity = 3

        self.bird_space = 150
        self.bird_speed = 7
        self.bird_x = 90
        self.bird_size = Point(x=25, y=25)
        
        self.tube_speed = 7
        self.tube_space = 500

        self.collide = collide

        self.next_bottom_tube = None


    def start(self, n_birds):
        for _ in range(n_birds):
            self.bird_group.add(
                Bird(
                    size=self.bird_size,
                    speed=self.bird_speed, 
                    gravity=self.gravity, 
                    x=self.bird_x,
                    y=int(self.screen_size.y/2)
                )
            )
        n_tubes = int((self.screen_size.x - self.bird_x)/self.tube_space) + 2
        for i in range(n_tubes):
            self.render_tube_pair()
        self.next_bottom_tube = self.bottom_tube_group.sprites()[0]


    def end_game(self, bird):
        self.surface.blit(
            self.font_end.render('Fim!!', True, (255, 255, 255)),
            (self.screen_size.x / 2 - 150, 50),
        )
        self.surface.blit(
            self.font_end.render(f'Max Pontos: {self.points}', True, (255, 255, 255)),
            (self.screen_size.x / 2 - 300, 170),
        )
        self.surface.blit(
            self.font_end.render(f'Bird: {bird.id}', True, (255, 255, 255)),
            (self.screen_size.x / 2 - 400, 290),
        )
        pygame.display.update()
        pygame.time.delay(5000)
        pygame.quit()


    def render_tube_pair(self):
        bottom_tube = Tube(tube_type='bottom', speed=self.tube_speed)
        top_tube = Tube('top', speed=self.tube_speed)

        img_size = Point(*bottom_tube.image.get_size())
        img_center = Point(x=img_size.x / 2, y=img_size.y / 2)

        bottom_max_size = min(self.screen_size.y - self.bird_space, img_size.y)

        bottom_tube.size = Point(x=img_size.x, y=randint(50, bottom_max_size))
        top_tube.size = Point(x=img_size.x, y = self.screen_size.y - bottom_tube.size.y - self.bird_space)

        bottom_y = self.screen_size.y - (bottom_tube.size.y - img_center.y)
        top_y = top_tube.size.y - img_center.y
        
        tubes = self.tube_group.sprites()
        x = self.screen_size.x if len(tubes) == 0 else tubes[-1].rect.x + self.tube_space

        bottom_tube.define_position(x, bottom_y)
        top_tube.define_position(x, top_y)
        self.tube_group.add(bottom_tube)
        self.tube_group.add(top_tube)
        self.bottom_tube_group.add(bottom_tube)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
                return True
        return False

    def draw_score(self):
        birds = sorted(self.bird_group.sprites(), key=lambda bird: bird.points)

        for i, bird in enumerate(birds[0:5]):
            self.surface.blit(
                self.font_score.render(f'Bird: {bird.id} - Pontos: {bird.points}', True, (255, 255, 255)),
                (20, 20*(i+1)),
            )


    def update_frame(self, counter):
        self.clock.tick(self.fps)
        go_up = self.handle_events()
        self.surface.blit(self.background, (0, 0))
        
        if self.next_bottom_tube.rect.x + self.next_bottom_tube.size.x <= self.bird_x - self.bird_size.x/2:
            self.next_bottom_tube = self.bottom_tube_group.sprites()[1]
            self.points += 1
            self.render_tube_pair()

        bird = self.bird_group.sprites()[0]
        if bird.rect.y + self.bird_size.y * 2 > self.next_bottom_tube.rect.y:
            go_up = True

        collision = pygame.sprite.groupcollide(self.bird_group, self.tube_group, False, False)

        if collision and self.collide:
            for bird in collision.keys():
                if len(self.bird_group.sprites()) == 1:
                    self.end_game(bird)
                bird.kill()

        self.tube_group.draw(self.surface)
        self.bird_group.draw(self.surface)

        self.draw_score()

        self.tube_group.update()
        self.bird_group.update(points=self.points, go_up=go_up)
        pygame.display.update()
