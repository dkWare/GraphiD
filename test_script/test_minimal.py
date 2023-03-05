import ui
import arcade
import cProfile


class Minimum(ui.EventTemplate, arcade.Window):
    def __init__(self):
        super().__init__()
        ui.EventTemplate.init(self)

    def game_loop(self):
        arcade.run()

def main():
    game = Minimum()
    cProfile.runctx("game.game_loop()", globals(), locals())