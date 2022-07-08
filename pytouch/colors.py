from collections import namedtuple
from typing import Sequence
from random import choice
from pathlib import Path
from os import listdir
import pickle
import yaml

import pyxel as px

from constants import COLORS_PATH, DATA_PATH, ColorIndexes


ColorsPalette = namedtuple('ColorsPalette', 'bg user_circ reach_circ')

DEFAULT_COLORS = (
    ColorsPalette(0xE5EDF3, 0x121922, 0x121922),
    ColorsPalette(0xFFFFFF, 0x121922, 0x121922),
    ColorsPalette(0xF5A8CA, 0xEAF3FC, 0xEAF3FC),
    ColorsPalette(0xF5A8CA, 0xE7C8E7, 0xE7C8E7),
    ColorsPalette(0x83D2BB, 0x0A1624, 0x0A1624),
)


def get_filenames() -> tuple:
    return ('default', *tuple(fn[:-5] for fn in sorted(listdir(COLORS_PATH)) if '.yaml' in fn))


def load_filename() -> str:
    path = DATA_PATH / 'colors.bin'
    if not path.exists():
        return ''
    return pickle.loads(path.read_bytes())


def is_filename_exists(filename: str) -> bool:
    return filename != '' and (COLORS_PATH / filename).exists()


def load_user_colors(filename: str) -> Sequence[ColorsPalette]:
    if 'default.yaml':
        return DEFAULT_COLORS

    data = yaml.safe_load((COLORS_PATH / filename).read_text())
    try:
        return tuple(
            ColorsPalette(
                *map(lambda color: eval(f'0x{color}'),
                    (colors['bg'], colors['user_circ'], colors['reach_circ'])
                )
            )
            for colors in data)
    except KeyError:
        raise KeyError(f'{filename} file reading error!')


def select_colors() -> Sequence[ColorsPalette]:
    filename = load_filename()
    if is_filename_exists(filename):
        return load_user_colors(filename)
    return DEFAULT_COLORS


def write_user_colors(filename: str):
    if not DATA_PATH.is_dir():
        DATA_PATH.mkdir()
    (DATA_PATH / 'colors.bin').write_bytes(pickle.dumps(filename))


class ColorPalette:
    def __init__(self):
        self._objs = ('bg', 'user_circ', 'reach_circ')
        self._current_color = 0
        self._colors = select_colors()

        px.colors[14] = px.colors[1]
        px.colors[15] = px.colors[7]

    @property
    def colors(self):
        return self._colors

    @colors.setter
    def colors(self, filename: str):
        self._current_color = 0
        self._colors = load_user_colors(filename)

    def update(self):
        for obj in self._objs:
            exec(f'px.colors[ColorIndexes.{obj}] = self._colors[self._current_color].{obj}')
        filtered_colors = filter(lambda color: color != self._current_color, range(len(self.colors)))
        self._current_color = choice(tuple(filtered_colors))
