from src.controllers import Game


game = Game()
game.start(n_birds=1)

counter = 0
while True:
    game.update_frame(counter)
    counter += 1
