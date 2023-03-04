from ui import (UIManager,
                UIGroup,
                MousePointer,
                RectButton)
import arcade


class Game(arcade.Window):
    def __init__(self):
        super().__init__(title="UI Test :)")
        self.mouse_pointer = MousePointer(0, 0)
        self.ui_manager = UIManager(self.mouse_pointer)

        self.quit_button = RectButton("BT_quit",
                                      center_x=100, center_y=100,
                                      width=100, height= 60,
                                      text="HALLO", text_size=10,
                                      text_dx=25, text_dy=10,
                                      ui_manager=self.ui_manager,
                                      release_event_outside_field=True)
        self.quit_button.debug = False
        self.quit_button.on_button_press = lambda b: arcade.close_window()

    def on_update(self, delta_time: float):
        self.ui_manager.update()

    def on_draw(self):
        self.ui_manager.draw()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pointer.change(x, y)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.ui_manager.raise_click_event_press(button)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.ui_manager.raise_click_event_release(button)


def main():
    Game()
    arcade.run()

if __name__ == "__main__":
    main()