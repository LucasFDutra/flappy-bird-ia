import pygame

from src import utils
from src.components import Bird, Tube

pygame.init()

screen_size = (960, 540)
surface = pygame.display.set_mode(size=screen_size)
clock = pygame.time.Clock()
font_end = pygame.font.SysFont('arial', 100)
font_score = pygame.font.SysFont('arial', 20)
fps = 120
bird_space = 150
previous_tube_distance = 600
tube_speed = 2

background = pygame.transform.scale(
    pygame.image.load('images/background.png'), size=screen_size
)

tubes_group = pygame.sprite.Group()
bird_group = pygame.sprite.Group()

utils.start_game(n_birds=1, screen_size=screen_size, bird_group=bird_group)

counter = 0
points = 0

v = 0
while True:
    clock.tick(fps)

    utils.handle_events()
    surface.blit(background, (0, 0))

    if counter % fps == 0:
        (
            previous_tube_distance,
            bird_space,
            tube_speed,
        ) = utils.adjust_difficulty_parameters(
            points=points,
            previous_tube_distance=previous_tube_distance,
            bird_space=bird_space,
            tube_speed=tube_speed,
        )

        utils.render_tube_pair(
            tubes_group=tubes_group,
            screen_size=screen_size,
            bird_space=bird_space,
            previous_tube_distance=previous_tube_distance,
            tube_speed=tube_speed,
        )
        points += 1

        t0 = tubes_group.sprites()[0]
        print(
            f'posição tubo {t0.rect.x} - count {counter} - vel: {v - t0.rect.x}'
        )
        v = t0.rect.x

    if (
        pygame.sprite.groupcollide(bird_group, tubes_group, False, False)
        and 1 == 0
    ):
        utils.end_game(
            surface=surface,
            screen_size=screen_size,
            font_end=font_end,
            distance=points,
        )

    tubes_group.draw(surface)
    bird_group.draw(surface)
    utils.update_scoreboard(
        surface=surface, font_score=font_score, points=points
    )
    tubes_group.update()
    bird_group.update()
    pygame.display.update()
    counter += 1
