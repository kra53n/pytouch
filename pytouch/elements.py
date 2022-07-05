from random import randint
import itertools

import pyxel as px

from constants import (Screen, GAP_BETWEEN_RADII, SYMBOL_WDT,
                       SYMBOL_HGT, SYMBOL_SPACE, MENU_BUTTONS_PADDING)


class Text:
    def __init__(self, text, x=None, y=None, col=2):
        self._text = text
        self.x = x
        self.y = y
        self.col = col

        self._process_coord()

    def get_wdt(self):
        return (SYMBOL_WDT + SYMBOL_SPACE) * len(self._text) - SYMBOL_SPACE

    def _process_coord(self):
        if self.x is None:
            self.x = (Screen.width - self.get_wdt()) // 2
        if self.y is None:
            self.y = (Screen.height - SYMBOL_HGT) // 2

    def get_coords(self):
        return (self.x, self.y), (self.x + self.get_wdt(), self.y + SYMBOL_HGT)

    def draw(self):
        px.text(self.x, self.y, self._text, self.col)


class Score:
    def __init__(self, padding_right=2, padding_top=2):
        self._padding_right = padding_right
        self._padding_top = padding_top
        self.score = 0

    def draw(self):
        px.text(self._padding_right, self._padding_top,
                   f"Score: {self.score}", (Screen.bg - 2) % 16)


class Button:
    def __init__(self, text, bg_col, fg_col, w=None, h=None):
        self.w = w
        self.h = h
        self.bg_col = bg_col
        self.fg_col = fg_col

        self._text = Text(text, self.w, self.h, self.fg_col)
        self.pressed = False
        self.hovered = False

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, text):
        self._text = Text(text, self.w, self.h, self.fg_col)

    def is_hovered(self):
        x, y = self._text.x, self._text.y
        w, h = self._text.get_wdt(), SYMBOL_HGT
        return x <= px.mouse_x <= x + w and y <= px.mouse_y <= y + h

    def __call__(self):
        self.process()
        self.draw()

    def process(self):
        if not self.is_hovered():
            return
        self.pressed = px.btnp(px.MOUSE_BUTTON_LEFT)
        self._text.col = (self.fg_col - 4) % 16

    def draw(self):
        self._text.draw()
        self._text.col = self.fg_col


class ButtonWithArrow(Button):
    def __init__(self, text, bg_col, fg_col, w=None, h=None):
        super().__init__(text, bg_col, fg_col, w, h)

        self.x = self._text.x
        self.y = self._text.y

        self.arrow = '10001 01010 00100'.split()
        self.frame = 0
        self.max_frame = len(self.arrow)

    def is_hovered(self):
        x, y = self._text.x, self._text.y
        w, h = self._text.get_wdt(), SYMBOL_HGT

        x -= self.frame + 1

        return x <= px.mouse_x <= x + w and y <= px.mouse_y <= y + h

    def _process_frames(self):
        if self.is_hovered():
            self.frame = self.frame + 1 if self.frame < self.max_frame else self.frame
        else:
            self.frame = self.frame - 1 if self.frame + 1 else self.frame

    def _process_arrow(self):
        # arrow coords
        x = self.x
        y = self.y

        to_draw = self.arrow[:self.frame+1]

        # move text from arrow to right side
        self._text.x = self.x + len(to_draw) + (1 if to_draw else 0)

        for row, col in enumerate(to_draw):
            for p_idx, p in enumerate(col):
                if p == '0':
                    continue
                px.pset(row + x, p_idx + y, self.fg_col)

    def draw(self):
        self._text.draw()
        self._process_frames()
        self._process_arrow()
        self._text.col = self.fg_col


class OptionChooser(Text):
    def __init__(self, title: str, title_col: int, opt_col: int, opts: tuple[str], x=None, y=None):
        super().__init__(title, x, y, title_col)
        self.opt_col = opt_col

        self.current_opt: int = 0
        self.opts = opts
        self.opts_len: int = len(self.opts)

    def process(self):
        one_of_keys = lambda *keys: any(map(lambda key: px.btnp(key), keys))

        if one_of_keys(px.KEY_UP, px.KEY_W):
            self.current_opt -= 1
            if self.current_opt < 0:
                self.current_opt = 0

        if one_of_keys(px.KEY_DOWN, px.KEY_S):
            self.current_opt += 1
            if self.current_opt > self.opts_len - 1:
                self.current_opt = self.opts_len - 1

    def draw(self):
        px.text(self.x, self.y, self._text, self.col)
        px.text(self.x + self.get_wdt(), self.y, self.opts[self.current_opt], self.opt_col)


class Circle:
    def __init__(self):
        self.r = 0
        self.col = (Screen.bg - 1) % 16
        self.x = 0
        self.y = 0

    def increase(self, size=1):
        self.r += size

    def draw(self, x, y):
        self.x = x
        self.y = y
        px.circ(self.x, self.y, self.r, self.col)


class ReachCircle(Circle):
    def __init__(self):
        super().__init__()
        self.min_r = 10
        self.respawn()

    def is_collided_with_circ(self, circ: Circle):
        x = abs(self.x - circ.x)
        y = abs(self.y - circ.y)

        return self.x - x + self.r <= circ.x - x + circ.r + GAP_BETWEEN_RADII and \
            self.y - y + self.r <= circ.y - y + circ.r + GAP_BETWEEN_RADII and \
            abs(self.r - circ.r) <= GAP_BETWEEN_RADII

    def respawn(self):
        self.x = randint(self.r, Screen.width - self.r)
        self.y = randint(self.r, Screen.height - self.r)
        self.r = randint(self.min_r, min(Screen.width, Screen.height) // 2) - 4

    def draw(self):
        px.circb(self.x, self.y, self.r, self.col)


def construct_buttons_in_center(button_obj: Button | ButtonWithArrow,
        buttons_names: tuple, bg: int, fg: int) -> dict:

        padding = MENU_BUTTONS_PADDING + SYMBOL_HGT
        buttons_block = len(buttons_names) * padding - MENU_BUTTONS_PADDING
        ys = itertools.count((Screen.height - buttons_block) // 2, padding)

        buttons = {}
        for button, y in zip(buttons_names, ys):
            buttons[button] = button_obj(button.capitalize(), bg, fg, None, y)
        return buttons
