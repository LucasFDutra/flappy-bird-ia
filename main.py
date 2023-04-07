from sys import argv
from src.controllers import Game

collide = True
n_birds = 1

for arg in argv:
    if arg == '-c=off':
        collide = False
    elif '-n=' in arg:
        n_birds = int(arg.split('=')[1])


game = Game(collide)

game.start(n_birds)

counter = 0
while True:
    game.update_frame(counter)
    counter += 1
