import GraphiD as ui
import arcade
import cProfile


class Game(ui.EventTemplate, arcade.Window):
    def __init__(self):
        super().__init__()
        ui.EventTemplate.init(self)
        self.ui_manager: ui.UIManager
        self.mouse_pointer: ui.MousePointer

        self.group = ui.UIGroup("GR_names", self.mouse_pointer)
        for y in range(500, -200, -30):
            ui.RectButton(str(y)+"button",
                          center_x=300, center_y=y,
                          width=380, height=50,
                          text=str(y)+" button", text_size=25,
                          text_dx=0, text_dy=0,
                          ui_manager=self.group).debug = False

        self.scroll_bar = ui.ScrollBar("scroll",
                                       center_x=300, center_y=500,
                                       width=400, height=600,
                                       thumb_bar_width=20,
                                       ui_manager=self.ui_manager,
                                       scroll_group=self.group,
                                       first_field=self.group.field_list[0],
                                       last_field=self.group.field_list[-1])
        self.ui_manager.register(self.group)

    def game_loop(self):
        arcade.run()

def main():
    game = Game()
    cProfile.runctx("game.game_loop()", globals(), locals())
