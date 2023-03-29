import pygame
from src.components import Tube, Bird

pygame.init()

screen_size = (960, 540)
surface = pygame.display.set_mode(size=screen_size)
clock = pygame.time.Clock()
font_end = pygame.font.SysFont('arial', 100)
font_score = pygame.font.SysFont('arial', 20)

background = pygame.transform.scale(
    pygame.image.load('images/background.png'), 
    size=screen_size
)


tubes_group = pygame.sprite.Group()
bird_group = pygame.sprite.GroupSingle(Bird(screen_size))

counter = 0
points = 0

def lost_function(distance):
    surface.blit(
        font_end.render('Perdeu!!', True, (255,255,255)),
        (screen_size[0]/2 - 150, screen_size[1]/2)
    )
    surface.blit(
        font_end.render(f'Distância: {distance}', True, (255,255,255)),
        (screen_size[0]/2 - 220, screen_size[1]/2 + 100)
    )
    pygame.display.update()
    pygame.time.delay(2000)
    pygame.quit()

while True:
    clock.tick(120)
    if counter % 120 == 0:
        tubes = tubes_group.sprites()
        if len(tubes) > 0:
            last_tube = tubes[-1]
        else:
            last_tube = None

        bottom_tube = Tube(is_top=False, screen_size=screen_size, other_tube=None, last_tube=last_tube)
        top_tube = Tube(is_top=True, screen_size=screen_size, other_tube=bottom_tube, last_tube=last_tube)
        tubes_group.add(bottom_tube)
        tubes_group.add(top_tube)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


    surface.blit(background, (0,0))
    if pygame.sprite.groupcollide(bird_group, tubes_group, False, False):
        lost_function(points)

    tubes_group.draw(surface)
    bird_group.draw(surface)
    
    surface.blit(
        font_score.render(f'Distância: {points}', True, (255,255,255)),
        (20,20)
    )
    tubes_group.update()
    bird_group.update(lost_function, points)
    pygame.display.update()
    counter += 1
    points = counter//120