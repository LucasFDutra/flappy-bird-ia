import pygame

from src.components import Bird, Tube


def start_game(n_birds, screen_size, bird_group):
    for _ in range(n_birds):
        bird_group.add(Bird(screen_size))


def end_game(surface, screen_size, font_end, distance):
    surface.blit(
        font_end.render('Perdeu!!', True, (255, 255, 255)),
        (screen_size[0] / 2 - 150, screen_size[1] / 2),
    )
    surface.blit(
        font_end.render(f'Distância: {distance}', True, (255, 255, 255)),
        (screen_size[0] / 2 - 220, screen_size[1] / 2 + 100),
    )
    pygame.display.update()
    pygame.time.delay(1000)
    pygame.quit()


def get_previus_tube(tubes_group):
    tubes = tubes_group.sprites()
    if len(tubes) > 0:
        return tubes[-1]


def update_scoreboard(surface, font_score, points):
    surface.blit(
        font_score.render(f'Distância: {points}', True, (255, 255, 255)),
        (20, 20),
    )


def render_tube_pair(
    tubes_group, screen_size, bird_space, previous_tube_distance, tube_speed
):
    previus_tube = get_previus_tube(tubes_group=tubes_group)

    bottom_tube = Tube(
        tube_type='bottom',
        speed=tube_speed,
        screen_size=screen_size,
        other_tube=None,
        previous_tube=previus_tube,
        bird_space=bird_space,
        previous_tube_distance=previous_tube_distance,
    )
    top_tube = Tube(
        tube_type='top',
        speed=tube_speed,
        screen_size=screen_size,
        other_tube=bottom_tube,
        previous_tube=previus_tube,
        bird_space=bird_space,
        previous_tube_distance=previous_tube_distance,
    )

    tubes_group.add(bottom_tube)
    tubes_group.add(top_tube)


def handle_events():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


def adjust_difficulty_parameters(
    points, previous_tube_distance, bird_space, tube_speed
):
    if points % 5 == 0 and points > 0:
        previous_tube_distance = (
            100
            if previous_tube_distance <= 100
            else previous_tube_distance - 50
        )
    if points % 10 == 0 and points > 0:
        bird_space = 70 if bird_space <= 70 else bird_space - 20
    if points % 10 == 0 and points > 0:
        tube_speed += 1

    return previous_tube_distance, bird_space, tube_speed
