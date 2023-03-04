from ui import UIManager, UIGroup, RectButton
import arcade


class Game(arcade.Window):
    def __init__(self):
        super().__init__(title="UI Test :)")

def main():
    Game()
    arcade.run()