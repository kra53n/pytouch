from enum import Enum

import pyxel as px

from elements import OptionChooser, one_of_keys, get_y_positions_in_center
from colors import get_filenames as get_colors_filenames
from constants import Screen
from music import Music


class State(Enum):
    NONSELECTED = 0
    SELECTED = 1


class Settings:
    def __init__(self, music: Music):
        self.state = State.NONSELECTED
        self.music = music
        
        _x = Screen.width // 2 - 30
        _ys = get_y_positions_in_center(3)
        self._selected_obj = 0
        self._selected_obj_col = 11
        self._nonselected_obj_col = 15

        self.color_chooser = OptionChooser('Colors: ', self._selected_obj_col, 13,
            get_colors_filenames(), _x, _ys[0])
        self.sound_level = OptionChooser('Sound level: ', self._nonselected_obj_col, 13,
            tuple(f'{round(100 * i / 7)}%' for i in range(8)), _x, _ys[1])
        self.effects_level = OptionChooser('Effects level: ', self._nonselected_obj_col, 13,
            tuple(f'{round(100 * i / 7)}%' for i in range(8)), _x, _ys[2])

        self.sound_level.current_opt = int(self.music.settings['music'])
        self.effects_level.current_opt = int(self.music.settings['effects'])

        self.objs = (self.color_chooser, self.sound_level, self.effects_level)
        self.objs_len = len(self.objs)

    def _update_colors(self):
        self.objs[self._selected_obj].col = self._selected_obj_col

        if self._selected_obj == 0:
            self.objs[self._selected_obj + 1].col = self._nonselected_obj_col
        elif self._selected_obj == self.objs_len - 1:
            self.objs[self._selected_obj - 1].col = self._nonselected_obj_col
        else:
            self.objs[self._selected_obj + 1].col = self._nonselected_obj_col
            self.objs[self._selected_obj - 1].col = self._nonselected_obj_col

    def process(self):
        if one_of_keys(px.KEY_RETURN, px.KEY_SPACE):
            self.state = State.SELECTED
        if px.btnp(px.KEY_ESCAPE):
            self.state = State.NONSELECTED

        match self.state:
            case State.NONSELECTED:

                if one_of_keys(px.KEY_UP, px.KEY_W):
                    self._selected_obj -= 1
                    if self._selected_obj < 0:
                        self._selected_obj = 0
                    self._update_colors()

                if one_of_keys(px.KEY_DOWN, px.KEY_S):
                    self._selected_obj += 1
                    if self._selected_obj >= self.objs_len:
                        self._selected_obj = self.objs_len - 1
                    self._update_colors()

            case State.SELECTED:
                self.objs[self._selected_obj].process()

    def write_settings(self, filename: str):
        pass

    def draw(self):
        px.cls(14)
        for obj in self.objs:
            obj.draw()

