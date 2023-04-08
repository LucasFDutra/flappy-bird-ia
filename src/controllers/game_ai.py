from src.components import Bird
from src.AI import BirdAI
from src.controllers.game import Game


class GameAI(Game):
    def __init__(self, collide) -> None:
        super().__init__(collide)
        self.birds_ai = {}

    def create_bird(self):
        bird = Bird(
            size=self.bird_size,
            speed=self.bird_speed, 
            gravity=self.gravity, 
            x=self.bird_x,
            y=int(self.screen_size.y/2)
        )    
        self.birds_ai[bird.id] = BirdAI(bird)
        return bird

    def handle_collision(self, collision):
        for bird in collision.keys():
            bird.kill()

    def handle_controll_event(self):
        bottom_tube_high = self.next_bottom_tube.rect.y 
        top_tube_high = bottom_tube_high - self.bird_space
        for bird_ai in self.birds_ai.values():
            bird_ai.play(bottom_tube_high, top_tube_high)

    def reset(self):
        self.next_bottom_tube = None
        for tube in self.tube_group.sprites():
            tube.kill()

        self.points = 0