from src.AI import BirdAI
from src.controllers.game import Game


class GameAI(Game):
    def __init__(self, collide) -> None:
        super().__init__(collide)
        self.birds_ai = {}
        self.gen = 0
        self.in_training = False
        self.min_birds_per_gen = 0
        self.old_gen_points = {}
        self.max_variation = 0.2

    def add_birds_ai(self, nn_config=None):
        for bird in self.bird_group.sprites():
            self.birds_ai[bird.id] = BirdAI(bird, nn_config, max_variation=self.max_variation)

    def handle_collision(self, collision):
        birds_to_die = sorted(list(collision.keys()), key=lambda bird: bird.ai_points)
        for bird in birds_to_die:
            del self.birds_ai[bird.id]
            bird.kill()
            if len(self.bird_group.sprites()) == self.min_birds_per_gen:
                break

    def handle_controll_event(self):
        bottom_tube_high = self.next_bottom_tube.rect.y 
        top_tube_high = bottom_tube_high - self.bird_space
        for bird_ai in self.birds_ai.values():
            bird_ai.play(bottom_tube_high, top_tube_high)

    def draw_score(self):
        row_space = 20
        for i, bird in enumerate(self.bird_group.sprites()[0:5]):
            self.surface.blit(
                self.font_score.render(f'Bird: {bird.id} - Pontos: {bird.points}', True, self.score_color),
                (20, row_space*(i+1)),
            )

        if self.in_training:
            self.surface.blit(
                self.font_score.render('-------------------------------------', True, self.score_color),
                (20, row_space*(i+2)),
            )

            self.surface.blit(
                self.font_score.render(f'Qty Birds: {len(self.bird_group.sprites())}', True, self.score_color),
                (20, row_space*(i+3)),
            )

            self.surface.blit(
                self.font_score.render(f'Geração: {self.gen}', True, self.score_color),
                (20, row_space*(i+4)),
            )
            self.surface.blit(
                self.font_score.render('-------------------------------------', True, self.score_color),
                (20, row_space*(i+5)),
            )

            for j, gen in enumerate(list(self.old_gen_points.keys())[-5:]):
                self.surface.blit(
                    self.font_score.render(f'Geração {gen}: {self.old_gen_points[gen]}', True, self.score_color),
                    (20, row_space*(i+6+j)),
                )


    def reset(self):
        self.next_bottom_tube = None
        for tube in self.tube_group.sprites():
            tube.kill()

        for bird in self.bird_group.sprites():
            bird.kill()

        self.points = 0
        self.birds_ai = {}

    def get_birds_config(self):
        return [bird_ai.get_config() for bird_ai in self.birds_ai.values()]

    def next_gen(self, birds_config):
        for i, bird in enumerate(self.bird_group.sprites()):
            nn_config = birds_config[i%len(birds_config)]
            self.birds_ai[bird.id] = BirdAI(bird, nn_config, max_variation=self.max_variation)
            self.birds_ai[bird.id].mutate()
            
