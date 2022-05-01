from random import randint
import pyxel

from constants import Screen
import cursors


class Text:
    def __init__(self, text):
        self._text = text

        self._symbol_len = 3
        self._padding_len = 1

    def _count_text_len(self):
        return (
            self._symbol_len + self._padding_len
        ) * len(self._text) - self._padding_len
    
    def _x_text_center_position(self):
        return (Screen.width - self._count_text_len()) // 2

    def draw(self):
        pyxel.text(self._x_text_center_position(), 0, self._text, 2)


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
