from sys import argv
from src.controllers import Game
from src.controllers import GameAI

collide = True
n_birds = 1
n_generations = 10
use_ai = False

for arg in argv:
    if arg == '-c=off':
        collide = False
    elif '-n=' in arg:
        n_birds = int(arg.split('=')[1])
    elif '-ia' in arg:
        use_ai = True
    elif '-ng=' in arg:
        n_generations = int(arg.split('=')[1])


def human_game():
    game = Game(collide)
    game.start(n_birds=1)
    while True:
        game.update_frame()

def ai_game():
    game = GameAI(collide)
    game.tube_speed = 10
    game.bird_space = 80
    game.start(n_birds=n_birds)
    count = 0
    while True:
        game.update_frame()
        if game.points >= 100 or len(game.bird_group.sprites()) <= 2:
            game.reset()
            game.start(n_birds)
            count += 1
        if count > n_generations:
            game.end_game()


if use_ai: ai_game()
else: human_game()
