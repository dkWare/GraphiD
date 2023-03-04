import arcade
import ui


class TicTacToeButton(ui.RectButton):
    def __init__(self, game, row, column, center_x, center_y, ui_manager):
        self.row = row
        self.column = column
        self.game = game

        super().__init__(f"b{row}|{column}",
                         text="",
                         text_size=14,
                         text_dx=0,
                         text_dy=0,
                         center_x=center_x,
                         center_y=center_y,
                         height=150,
                         width=150,
                         color_masked=arcade.color.WHITE_SMOKE,
                         color_unmasked=arcade.color.ASH_GREY,
                         ui_manager=ui_manager,
                         release_event_outside_field=True)

        self.debug = False

    def on_button_press(self, button):
        self.game.on_board_click(self.row, self.column)


class TicTacToe(arcade.Window):
    def __init__(self):
        super().__init__(600, 600, "Tic-Tac-Toe")
        
        # Öffne ein Dialogfenster und frage den Benutzer, ob er fortfahren möchte.
        if arcade.confirm_dialog("Bestätigung", "Möchten Sie wirklich fortfahren?"):
            print("Der Benutzer hat die Bestätigungsfrage akzeptiert.")
        else:
            print("Der Benutzer hat die Bestätigungsfrage abgelehnt.")

        self.mouse_pointer = ui.MousePointer(0, 0)
        self.gui_manager = ui.UIManager(self.mouse_pointer)

        self.board = [[None, None, None],
                      [None, None, None],
                      [None, None, None]]

        self.turn = 'X'
        self.winner = None

        self.create_board()
        self.create_reset_button()

    def create_board(self):
        for row in range(3):
            for column in range(3):
                button = TicTacToeButton(self, row, column, 100 + column * 190, 500 - row * 100, self.gui_manager)
                self.board[row][column] = button

    def create_reset_button(self):
        reset_button = ui.RectButton("reset",text="Reset",
                                      center_x=100,
                                      center_y=100,
                                      height=50,
                                      width=100,
                                      text_size=14,
                                      text_dx=0,
                                      text_dy=0,
                                      color_masked=arcade.color.WHITE_SMOKE,
                                      color_unmasked=arcade.color.ASH_GREY,
                                      ui_manager=self.gui_manager,
                                      release_event_outside_field=True)
        reset_button.on_button_press = lambda button: self.reset_game()

    def reset_game(self):
        for row in range(3):
            for column in range(3):
                self.board[row][column].set_text("")
                self.board[row][column].set_locked(False)
                self.board[row][column].color_unmasked = arcade.color.ASH_GREY
                self.board[row][column].color_masked = arcade.color.WHITE_SMOKE
        self.turn = 'X'
        self.winner = None

    def on_board_click(self, row, column):
        button = self.board[row][column]
        if not button.IS_LOCKED:
            button.text = self.turn
            self.check_for_winner()
            if not self.winner:
                self.change_turn()

    def change_turn(self):
        if self.turn == 'X':
            self.turn = 'O'
        else:
            self.turn = 'X'

    def check_for_winner(self):
        # check rows
        for row in self.board:
            if all(cell.text == 'X' for cell in row):
                self.declare_winner('X')
                return
            elif all(cell.text == 'O' for cell in row):
                self.declare_winner('O')
                return

        # check columns
        for col in range(3):
            if self.board[0][col].text == self.board[1][col].text == self.board[2][col].text == 'X':
                self.declare_winner('X')
                return
            elif self.board[0][col].text == self.board[1][col].text == self.board[2][col].text == 'O':
                self.declare_winner('O')
                return

        # check diagonals
        if self.board[0][0].text == self.board[1][1].text == self.board[2][2].text == 'X':
            self.declare_winner('X')
            return
        elif self.board[0][0].text == self.board[1][1].text == self.board[2][2].text == 'O':
            self.declare_winner('O')
            return
        elif self.board[0][2].text == self.board[1][1].text == self.board[2][0].text == 'X':
            self.declare_winner('X')
            return
        elif self.board[0][2].text == self.board[1][1].text == self.board[2][0].text == 'O':
            self.declare_winner('O')
            return

        # check for tie
        if all(cell.text != "" for row in self.board for cell in row):
            self.declare_tie()

    def declare_winner(self, winner):
        self.winner = winner
        for row in self.board:
            for cell in row:
                if cell.text == winner:
                    cell.set_color_locked(arcade.color.GREEN)
                else:
                    cell.set_color_locked(arcade.color.RED)
                cell.set_locked(True)

    def declare_tie(self):
        self.winner = 'Tie'
        for row in self.board:
            for cell in row:
                cell.set_color_locked(arcade.color.RED)
                cell.set_locked(True)

    def on_draw(self):
        arcade.start_render()
        self.gui_manager.draw()

    def on_update(self, delta_time):
        self.gui_manager.update()

    def on_mouse_motion(self, x, y, dx, dy):
        self.mouse_pointer.change(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        self.gui_manager.raise_click_event_press(button)

    def on_key_press(self, symbol, modifiers):
        if symbol == arcade.key.SPACE:
            self.reset_game()

    def reset_game(self):
        self.turn = 'X'
        self.winner = None
        for row in self.board:
            for cell in row:
                cell.text = ''
                cell.set_locked(False)
                cell.set_color_locked(arcade.color.RED)

    def setup(self):
        self.board = [[Cell(x, y) for x in range(3)] for y in range(3)]
        self.mouse_pointer = ui.MousePointer(0, 0)

        self.gui_manager.add_ui_element(arcade.SpriteList())
        self.gui_manager.add_ui_element(self.mouse_pointer)

        for row in self.board:
            for cell in row:
                self.gui_manager.add_ui_element(cell)

    def run(self):
        arcade.run()
