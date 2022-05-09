import pyxel

from elements import Button


class Menu:
    def __init__(self):
        self.colors = {"bg": 1, "fg": 2}
        wdt = 40
        self.buttons = {
            "play": Button('Play', self.colors['bg'], self.colors['fg'], None, 30),
            "settings": Button('Settings', self.colors['bg'], self.colors['fg'], None, 50),
            "exit": Button('Exit', self.colors['bg'], self.colors['fg'], None, 70),
        }
        self.is_drawing = True

    def update(self):
        if self.buttons['play'].pressed:
            self.buttons['play'].pressed = False
            self.is_drawing = False
        if self.buttons['exit'].pressed:
            pyxel.quit()
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            self.is_drawing = True

    def draw(self):
        if not self.is_drawing:
            return

        pyxel.cls(self.colors['bg'])
        for button_key in self.buttons.keys():
            self.buttons[button_key]()
