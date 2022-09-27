from random import randint
from collections import namedtuple

import pyxel as px

from constants import (Screen, GAP_BETWEEN_RADII, SYMBOL_WDT,
                       SYMBOL_HGT, SYMBOL_SPACE, MENU_BUTTONS_PADDING,
                       ColorIndexes)


def one_of_keys(*keys):
    return any(map(lambda key: px.btnp(key), keys))


Point = namedtuple('Point', ['x', 'y'])


class Camera:
    def __init__(self):
        self._offset = 3
        self._queue = []

    def update(self):
        if len(self._queue) and px.frame_count % 20:
            px.camera(*self._queue.pop(0))

    def shake(self):
        self._queue = [self._generate_offset_coords() for _ in range(10)] + [(0, 0),]

    def _generate_offset_coords(self):
        return (randint(-self._offset, self._offset),
                randint(-self._offset, self._offset))


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
                f"Score: {self.score}", ColorIndexes.reach_circ)


class Health:
    def __init__(self):
        self.max_health = 3
        self.health = 3
        self._hearts = (Point(0, 0), ) * self.max_health

        self._img = 0
        self._active_heart = Point(0, 0)
        self._nonactive_heart = Point(8, 0)
        self._size = 8
        self._colkey = 0

        self._padding = 2
        self._health = Point(Screen.width - (self._padding + self._size) * self.max_health, self._padding)

    def is_gameover(self):
        return self.health < 1

    def draw(self):
        x = self._health.x
        for heart in range(self.max_health):
            img_pos_x = self._active_heart.x if heart < self.health else self._nonactive_heart.x
            px.blt(x, self._health.y, self._img,
                   img_pos_x, self._active_heart.y, self._size, self._size, self._colkey)
            x += self._size + self._padding


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
        return all(x <= px.mouse_x <= x + w,
                   y <= px.mouse_y <= y + h)

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
        return all(x <= px.mouse_x <= x + w,
                   y <= px.mouse_y <= y + h)

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

        self.current_opt = 0
        self.opts = opts
        self.opts_len = len(self.opts)

    def process(self):
        if one_of_keys(px.KEY_UP, px.KEY_W):
            self.current_opt -= 1
            if self.current_opt < 0:
                self.current_opt = 0

        if one_of_keys(px.KEY_DOWN, px.KEY_S):
            self.current_opt += 1
            if self.current_opt > self.opts_len - 1:
                self.current_opt = self.opts_len - 1

    def get_option(self) -> str:
        return self.opts[self.current_opt]

    def draw(self):
        px.text(self.x, self.y, self._text, self.col)
        px.text(self.x + self.get_wdt(), self.y, self.get_option(), self.opt_col)


class Circle:
    def __init__(self):
        self.r = 0
        self.col = ColorIndexes.user_circ
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
        self.col = ColorIndexes.reach_circ
        self.min_r = 10
        self.respawn()

    def is_collided_with_circ(self, circ: Circle):
        x = abs(self.x - circ.x)
        y = abs(self.y - circ.y)
        return all(self.x - x + self.r <= circ.x - x + circ.r + GAP_BETWEEN_RADII,
                   self.y - y + self.r <= circ.y - y + circ.r + GAP_BETWEEN_RADII,
                   abs(self.r - circ.r) <= GAP_BETWEEN_RADII)

    def respawn(self):
        self.x = randint(self.r, Screen.width - self.r)
        self.y = randint(self.r, Screen.height - self.r)
        self.r = randint(self.min_r, min(Screen.width, Screen.height) // 2) - 4

    def draw(self):
        px.circb(self.x, self.y, self.r, self.col)


def get_y_positions_in_center(text_objs_num: int) -> tuple:
    padding = MENU_BUTTONS_PADDING + SYMBOL_HGT
    objs_block = text_objs_num * padding - MENU_BUTTONS_PADDING
    start_y = (Screen.height - objs_block) // 2
    return tuple(start_y + (i * padding) for i in range(text_objs_num))


def construct_buttons_in_center(button_obj: Button | ButtonWithArrow,
        buttons_names: tuple, bg: int, fg: int) -> dict:
    buttons = {}
    for button, y in zip(buttons_names, get_y_positions_in_center(len(buttons_names))):
        buttons[button] = button_obj(button.capitalize(), bg, fg, None, y)
    return buttons
