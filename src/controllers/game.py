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

        self.font_end = pygame.font.SysFont('arial', 30)
        self.font_score = pygame.font.SysFont('arial', 15)
        
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
        self.score_color = (0, 0, 0)


    def start(self, n_birds):
        for _ in range(n_birds):
            self.bird_group.add(
                Bird(
                    size=self.bird_size,
                    speed=self.bird_speed, 
                    gravity=self.gravity, 
                    x=self.bird_x,
                    y=randint(50, self.screen_size.y - 50)
                )
            )

        n_tubes = int((self.screen_size.x - self.bird_x)/self.tube_space) + 2
        for i in range(n_tubes):
            self.render_tube_pair()
        self.next_bottom_tube = self.bottom_tube_group.sprites()[0]

    def end_game(self):
        self.surface.blit(
            self.font_end.render('Fim!!', True, (255, 255, 255)),
            (self.bird_x, self.screen_size.y - 100),
        )
        self.surface.blit(
            self.font_end.render(f'Pontos: {self.points}', True, (255, 255, 255)),
            (self.bird_x, self.screen_size.y - 50),
        )
        pygame.display.update()
        pygame.time.delay(3000)
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
    
    def handle_controll_event(self):
        key = pygame.key.get_pressed()
        if key[pygame.K_SPACE]:
            for bird in self.bird_group.sprites():
                bird.go_up()
        else:
            for bird in self.bird_group.sprites():
                bird.go_down()

    def draw_score(self):
        for i, bird in enumerate(self.bird_group.sprites()[0:5]):
            self.surface.blit(
                self.font_score.render(f'Bird: {bird.id} - Pontos: {bird.points}', True, self.score_color),
                (20, 20*(i+1)),
            )

    def handle_collision(self, collision):
        for bird in collision.keys():
            if len(self.bird_group.sprites()) == 1:
                self.end_game()
            bird.kill()

    def update_frame(self):
        self.clock.tick(self.fps)
        self.handle_events()
        self.handle_controll_event()
        self.surface.blit(self.background, (0, 0))
        
        if self.next_bottom_tube.rect.x + self.next_bottom_tube.size.x <= self.bird_x - self.bird_size.x/2:
            self.next_bottom_tube = self.bottom_tube_group.sprites()[1]
            self.points += 1
            self.render_tube_pair()

        collision = pygame.sprite.groupcollide(self.bird_group, self.tube_group, False, False)

        if collision and self.collide:
            self.handle_collision(collision)

        self.tube_group.draw(self.surface)
        self.bird_group.draw(self.surface)

        self.draw_score()

        self.tube_group.update()
        self.bird_group.update(points=self.points)
        pygame.display.update()
