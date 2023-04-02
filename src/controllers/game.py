from random import randint

import pygame
from src.utils import Point
from src.components import Bird, Tube


class Game():
    def __init__(self) -> None:
        pygame.init()

        self.screen_size = Point(x=960, y=400)
        
        self.surface = pygame.display.set_mode(size=tuple(self.screen_size))
        self.clock = pygame.time.Clock()

        self.font_end = pygame.font.SysFont('arial', 100)
        self.font_score = pygame.font.SysFont('arial', 20)
        
        self.tube_group = pygame.sprite.Group()
        self.bird_group = pygame.sprite.Group()

        self.background = pygame.transform.scale(
            pygame.image.load('images/background.png'), size=tuple(self.screen_size)
        )
        
        self.points = 0
        self.fps = 120
        self.bird_space = 150
        self.bird_up_speed = 2
        self.bird_down_speed = 3
        self.bird_size = Point(x=25, y=25)

        self.tube_speed = 2
        self.previous_tube_distance = self.get_tube_distance()
        self.collide = False


    def start(self, n_birds, human):
        for i in range(n_birds):
            use_ia = False if human and i == 0 else True
            self.bird_group.add(
                Bird(
                    screen_size=self.screen_size, 
                    up_speed=self.bird_up_speed, 
                    down_speed=self.bird_down_speed, 
                    size=self.bird_size,
                    id=i,
                    tube_group=self.tube_group,
                    use_ia=use_ia
                )
            )


    def end_game(self, bird):
        bird_id = bird.id
        bird.lost_game()
        if len(self.bird_group) == 0:
            self.surface.blit(
                self.font_end.render('Fim!!', True, (255, 255, 255)),
                (self.screen_size.x / 2 - 150, 50),
            )
            self.surface.blit(
                self.font_end.render(f'Max Pontos: {self.points}', True, (255, 255, 255)),
                (self.screen_size.x / 2 - 300, 170),
            )
            self.surface.blit(
                self.font_end.render(f'Vencedor - Bird: {bird_id}', True, (255, 255, 255)),
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
        x = self.screen_size.x if len(tubes) == 0 else tubes[-1].rect.x + self.previous_tube_distance

        bottom_tube.define_position(x, bottom_y)
        top_tube.define_position(x, top_y)
        self.tube_group.add(bottom_tube)
        self.tube_group.add(top_tube)
        

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()


    def adjust_difficulty_parameters(self):
        rebuild_tubes = False
        bird_max_speed = max(self.bird_up_speed, self.bird_down_speed)
        tube_max_speed = 5

        if self.points % 5 == 0 and self.points > 0:
            min_bird_space = (self.bird_size.y + bird_max_speed) * 1.3
            if self.bird_space - min_bird_space*0.25 >= min_bird_space:
                self.bird_space = int(self.bird_space - min_bird_space*0.25)
                rebuild_tubes = True

        if self.points % 7 == 0 and self.points > 0:
            if self.tube_speed + 1 <= tube_max_speed:
                self.tube_speed += 1
                self.previous_tube_distance = self.get_tube_distance()
                rebuild_tubes = True

        if rebuild_tubes:
            for tube in self.tube_group.sprites():
                tube.speed = self.tube_speed
                if tube.rect.x > self.screen_size.x:
                    tube.kill()
            
            for _ in range(5):
                self.render_tube_pair()      


    def get_tube_distance(self):
        bird_min_speed = min(self.bird_up_speed, self.bird_down_speed)
        return int((self.tube_speed * self.screen_size.y) / bird_min_speed) + self.bird_size.y


    def update_frame(self, counter):
        self.clock.tick(self.fps)
        self.handle_events()
        self.surface.blit(self.background, (0, 0))

        if counter % self.fps == 0:
            self.adjust_difficulty_parameters()
            for _ in range(3):
                if len(self.tube_group.sprites()) < 20:
                    self.render_tube_pair()

        collision = pygame.sprite.groupcollide(self.bird_group, self.tube_group, False, False)

        if collision:
            for bird in collision.keys():
                self.end_game(bird)

        self.tube_group.draw(self.surface)
        self.bird_group.draw(self.surface)

        for i, bird in enumerate(self.bird_group.sprites()):
            self.surface.blit(
                self.font_score.render(f'Bird: {bird.id} - Pontos: {bird.points}', True, (255, 255, 255)),
                (20, 20*(i+1)),
            )

        self.points = counter//self.fps
        self.tube_group.update()
        self.bird_group.update(points=self.points)
        pygame.display.update()
