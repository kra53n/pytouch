import pyxel

from elements import Button


class Menu:
    def __init__(self):
        self.colors = {"bg": 1, "fg": 2}
        wdt = 40
        self.buttons = {
            "play": Button('Play', self.colors['bg'], self.colors['fg'], wdt),
            "settings": Button('Settings', self.colors['bg'], self.colors['fg'], wdt),
            "exit": Button('Exit', self.colors['bg'], self.colors['fg'], wdt),
        }
        self.is_drawing = True

    def __call__(self):
        self.draw()

    def draw(self):
        if not self.is_drawing:
            return

        pyxel.cls(self.colors['bg'])
        self.buttons['play']()


if __name__ == "__main__":
    Menu()
