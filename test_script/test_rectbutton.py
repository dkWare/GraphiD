import arcade
import cProfile
import GraphiD as ui


class Button(ui.RectButton):
    def __init__(self, manager, x, y, name, text_normal, text_enter):
        super().__init__(name,
                         center_x=x, center_y=y,
                         height=100, width=200,
                         text=text_normal, text_size=20,
                         text_dx=10, text_dy=15,
                         ui_manager=manager)
        self.text_normal = text_normal
        self.text_enter = text_enter

        self.manager = manager
        self.count = 10

    def on_button_press(self, button):
        self.text = "PRESSED"
        if self.ID == "Normal":
            button = self.manager["Locked"]
            if button.IS_LOCKED:
                button.set_locked(False)
            else:
                button.set_locked(True)

    def on_button_release(self, button):
        if self.ID == "SEC":
            self.count -= 1
            self.text = f"RELEASED: {self.count}"
            if self.count < 1:
                self.set_locked(True)
        else:
            self.text = "RELEASED"

    def on_mouse_enters(self):
        self.text = self.text_enter

    def on_mouse_leaves(self):
        self.text = self.text_normal
        if self.ID == "SEC":
            self.count = 10

    def on_lock(self):
        self.text = "LOCKED"

    def on_unlock(self):
        self.text = self.text_normal

class ChatWindow(arcade.Window):
    def __init__(self):
        super().__init__(800, 600, "TEST")
        self.mouse_pointer = ui.MousePointer(0, 0)
        self.gui_manager = ui.UIManager(self.mouse_pointer)

        Button(self.gui_manager, 100, 100, "Normal", "LOCK ABOVE", "!!DO IT!!")
        self.locked = Button(self.gui_manager, 100, 150, "Locked", "42", "106")
        sec = Button(self.gui_manager, 100, 200, "SEC", "PRESS 9x", "I LIKE IT")
        sec.set_color_unmasked(arcade.color.BLUE_BELL)
        sec.set_color_masked(arcade.color.BLUEBONNET)
        sec.set_color_pressed(arcade.color.SKY_BLUE)
        sec.set_color_locked(arcade.color.BLUE_GRAY)

    def button_event_lock(self, button_used):
        button = self.gui_manager["MoveButtonX"]
        if button.IS_LOCKED:
            button.set_locked(False)
        else:
            button.set_locked(True)

    def button_event_active(self, button_used):
        button = self.gui_manager["MoveButtonX"]
        if button.IS_ACTIVE:
            button.deactivate()
        else:
            button.activate()

    def on_draw(self):
        self.gui_manager.draw()

    def on_update(self, delta_time: float):
        self.gui_manager.update()

    def on_mouse_motion(self, x: int, y: int, dx: int, dy: int):
        self.mouse_pointer.change(x, y)

    def on_mouse_press(self, x: int, y: int, button: int, modifiers: int):
        self.gui_manager.raise_click_event_press(button)

    def on_mouse_release(self, x: int, y: int, button: int, modifiers: int):
        self.gui_manager.raise_click_event_release(button)

    def on_key_press(self, symbol: int, modifiers: int):
        if symbol == arcade.key.A:
            if self.locked.IS_LOCKED:
                self.locked.text = "NORMAL"
                self.locked.set_locked(False)
            else:
                self.locked.text = "LOCKED"
                self.locked.set_locked(True)

    def game_loop(self):
        arcade.run()

def main():
    game = ChatWindow()
    cProfile.runctx("game.game_loop()", globals(), locals())