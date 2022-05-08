from random import randint
import itertools

import pyxel

from constants import Screen
import cursors


class Text:
    def __init__(self, text, x=None, y=None, col=2):
        self._text = text
        self.x = x
        self.y = y
        self.col = col

        self.symbol_len_hori = 3
        self.symbol_len_vert = 5
        self._padding_len = 1

        self._process_coord()
    
    def text_wdt(self):
        return (self.symbol_len_hori + self._padding_len) * len(self._text) - self._padding_len

    def _process_coord(self):
        if self.x == None:
            self.x = (Screen.width - self.text_wdt()) // 2
        if self.y == None:
            self.y = (Screen.height - self.symbol_len_vert) // 2

    def get_coords(self):
        return (self.x, self.y), (self.x + self.text_wdt(), self.y + self.symbol_len_vert)
    
    def draw(self):
        pyxel.text(self.x, self.y, self._text, self.col)


class Score:
    def __init__(self, padding_right=2, padding_top=2):
        self._padding_right = padding_right
        self._padding_top = padding_top
        self.score = 0

    def increase(self):
        self.score += 1

    def reduce(self):
        self.score -= 1

    def draw(self):
        pyxel.text(self._padding_right, self._padding_top,
                f"Score: {self.score}", (Screen.bg - 2) % 16)


class Button:
    def __init__(self, text, bg_col, fg_col, w=None, h=None):
        self.text = Text(text, None, None, 7)
        self.pressed = False

        # self.arrow_state = None
        # self.arrow = (
        #     (
        #         '000',
        #         '000',
        #         '100',
        #         '000',
        #         '000',
        #     ),
        #     (
        #         '000',
        #         '100',
        #         '010',
        #         '100',
        #         '000',
        #     ),
        #     (
        #         '100',
        #         '010',
        #         '001',
        #         '010',
        #         '100',
        #     ),
        # )

    def __call__(self):
        self._process()
        self._draw()

    def _process(self):
        x, y = self.text.x, self.text.y
        w, h = self.text.text_wdt(), self.text.symbol_len_vert

        if not (x <= pyxel.mouse_x <= x + w):
            return
        if not (y <= pyxel.mouse_y <= y + h):
            return
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.pressed = True

        self.text.col = 3

    def _draw(self):
        self.text.draw()
        self.text.col = 7


class Circle:
    def __init__(self):
        self._r   = 0
        self._col = (Screen.bg - 1) % 16

    def zero(self):
        self._r = 0

    def increase(self, size=1):
        self._r += size

    @property
    def r(self):
        return self._r

    @r.setter
    def r(self, r):
        self._r = r

    @property
    def col(self):
        return self._col

    @col.setter
    def col(self, color):
        self._col = color
    
    def draw(self, x, y):
        pyxel.circ(x, y, self._r, self._col)


class ReachCircle(Circle):
    def __init__(self):
        super().__init__()
        self.min_r = 10
        self.respawn()

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def respawn(self):
        self._x = randint(self._r, Screen.width - self._r)
        self._y = randint(self._r, Screen.height - self._r)
        self._r = randint(self.min_r, min(Screen.width, Screen.height) // 2) - 4

    def draw(self):
        pyxel.circb(self._x, self._y, self._r, self._col)
