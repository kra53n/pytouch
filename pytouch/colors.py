from collections import namedtuple
from typing import Sequence
from pathlib import Path
from os import listdir
import pickle
import yaml


ColorsPalette = namedtuple('ColorsPalette', 'bg user_circ reach_circ')

DEFUALT_COLORS = (
    ColorsPalette(0xE5EDF3, 0x121922, 0x121922),
    ColorsPalette(0xFFFFFF, 0x121922, 0x121922),
    ColorsPalette(0xF5A8CA, 0xEAF3FC, 0xEAF3FC),
    ColorsPalette(0xF5A8CA, 0xE7C8E7, 0xE7C8E7),
    ColorsPalette(0x83D2BB, 0x0A1624, 0x0A1624),
)

COLORS_PATH = Path(__file__).parent / 'config'


def get_filenames() -> tuple:
    return ('defalut', *tuple(fn[:-5] for fn in sorted(listdir(COLORS_PATH)) if '.yaml' in fn))


def load_filename() -> str:
    path = Path('assets/colors.bin')
    if not path.exists():
        return ''
    return pickle.loads(path.read_bytes())


def is_filename_exists(filename: str) -> bool:
    return filename != '' and (COLORS_PATH / filename).exists()


def load_user_colors(filename: str) -> Sequence[ColorsPalette]:
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
    return DEFUALT_COLORS
