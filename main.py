from sys import argv
from src.controllers import Game
from src.controllers import GameAI
import json
from time import sleep
import matplotlib.pyplot as plt
from os import remove

collide = True
n_birds = 1
use_ai = False
ai_training = False

sleep_time = 0
tube_speed = 7
bird_space = 56
min_birds_per_gen = 3
max_points = 100
max_variation = 0.05
n_generations = 300
tube_space = 650

for arg in argv:
    if arg == '-c=off':
        collide = False
    elif '-n=' in arg:
        n_birds = int(arg.split('=')[1])
    elif '-iat=' in arg:
        ai_training = True
        ai_config_file = arg.split('=')[1]
    elif '-ia=' in arg:
        ai_config_file = arg.split('=')[1]
    elif '-ng=' in arg:
        n_generations = int(arg.split('=')[1])


def human_game():
    game = Game(collide)
    game.start(n_birds=1)
    while True:
        game.update_frame()

def ai_training_game(ai_config_file):
    game = GameAI(collide)
    game.in_training = True
    game.gen = 0
    game.min_birds_per_gen = min_birds_per_gen
    game.tube_speed = tube_speed
    game.bird_space = bird_space
    game.tube_space = tube_space
    game.max_variation = max_variation
    game.start(n_birds=n_birds)
    game.add_birds_ai()
    while True:
        game.update_frame()
        if len(game.bird_group.sprites()) <= min_birds_per_gen:
            sleep(sleep_time)
            game.old_gen_points[game.gen] = game.points
            birds_config = game.get_birds_config()
            game.reset()
            game.start(n_birds)
            game.next_gen(birds_config)
            game.gen += 1
        if game.points >= max_points or game.gen > n_generations:
            list(game.birds_ai.values())[0].save(ai_config_file)
            game.end_game()
            break
    plt.plot(list(game.old_gen_points.values()))
    plt.show()

def ai_game(ai_config_file):
    game = GameAI(collide)
    game.tube_speed = tube_speed
    game.bird_space = bird_space
    game.tube_space = tube_space
    game.start(n_birds=1)
    with open(ai_config_file, 'r') as f:
        config = json.load(f)
    game.add_birds_ai(config)
    while True:
        game.update_frame()
        if len(game.bird_group.sprites()) == 0 or game.points >= max_points:
            print(f'fim de jogo: {game.points}')
            game.end_game()
            break


if ai_training: ai_training_game(ai_config_file)
elif ai_config_file: ai_game(ai_config_file)
else: human_game()
