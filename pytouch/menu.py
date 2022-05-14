import pyxel

from constants import State
from elements import Button


class Menu:
    def __init__(self):
        self.colors = {"bg": 1, "fg": 7}
        self.buttons = {
            "play": Button('Play', self.colors['bg'], self.colors['fg'], None, 30),
            "settings": Button('Settings', self.colors['bg'], self.colors['fg'], None, 50),
            "exit": Button('Exit', self.colors['bg'], self.colors['fg'], None, 70),
        }

    def update(self, game_obj):
        if self.buttons['play'].pressed:
            game_obj.state = State.PLAY
            pyxel.mouse(False)
            self.buttons['play'].pressed = False

        if self.buttons['exit'].pressed:
            pyxel.quit()

        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.mouse(True)

    def draw(self):
        pyxel.cls(self.colors['bg'])
        for button_key in self.buttons.keys():
            self.buttons[button_key]()
