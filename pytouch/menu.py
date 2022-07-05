from itertools import count
import pyxel as px

from constants import State, Screen, SYMBOL_HGT, MENU_BUTTONS_PADDING
from elements import ButtonWithArrow, construct_buttons_in_center


class Menu:
    def __init__(self):
        self.colors = {'bg': 14, 'fg': 15}
        self.buttons = construct_buttons_in_center(
            ButtonWithArrow, ('play', 'settings', 'exit'), 14, 15)

    def update(self, game_obj):
        if self.buttons['play'].pressed:
            game_obj.state = State.PLAY
            px.mouse(False)
            self.buttons['play'].pressed = False
            self.buttons['play'].text = 'Continue'
            self.buttons['play'].x = self.buttons['play'].text.x
        elif self.buttons['settings'].pressed:
            game_obj.state = State.SETTINGS
            self.buttons['settings'].pressed = False
        elif self.buttons['exit'].pressed:
            px.quit()

    def draw(self):
        px.cls(self.colors['bg'])
        for button_key in self.buttons.keys():
            self.buttons[button_key]()
