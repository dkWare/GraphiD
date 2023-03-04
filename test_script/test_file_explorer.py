import ui
import arcade
import cProfile


class Game(ui.EventTemplate, arcade.Window):
    def __init__(self):
        super().__init__()
        self.mouse_pointer = ui.MousePointer(-10, -10, "mainPointer")
        self.gui_manager = ui.UIManager(self.mouse_pointer)

        self.scroll_bar = ui.ScrollBar("scroll",
                                       center_x=100, center_y=100,
                                       width=200, height=200,
                                       thumb_bar_width=20,
                                       ui_manager=self.gui_manager)

    def game_loop(self):
        arcade.run()

def main():
    game = Game()
    cProfile.runctx("game.game_loop()", globals(), locals())
