from enum import Enum

import pyxel as px

from elements import OptionChooser, one_of_keys, get_y_positions_in_center
from colors import get_filenames as get_colors_filenames
from data import load_data, write_file
from constants import Screen


class State(Enum):
    NONSELECTED = 'nonselected'
    SELECTED = 'selected'


class Settings:
    def __init__(self):
        self.state = State.NONSELECTED
        data = load_data()
        
        _x = Screen.width // 2 - 30
        _ys = get_y_positions_in_center(3)
        self._selected_obj = data['color_chooser']
        self._selected_obj_col = 11
        self._nonselected_obj_col = 15

        self.color_chooser = OptionChooser('Colors: ', self._selected_obj_col, 13,
            get_colors_filenames(), _x, _ys[0])
        self.sound_level = OptionChooser('Sound level: ', self._nonselected_obj_col, 13,
            tuple(f'{round(100 * i / 7)}%' for i in range(8)), _x, _ys[1])
        self.effects_level = OptionChooser('Effects level: ', self._nonselected_obj_col, 13,
            tuple(f'{round(100 * i / 7)}%' for i in range(8)), _x, _ys[2])

        self.color_chooser.current_opt = data['color_chooser'] if data['color_chooser'] < len(self.color_chooser.opts) else 0
        self.sound_level.current_opt = data['music']
        self.effects_level.current_opt = data['effects']

        self.objs = (self.color_chooser, self.sound_level, self.effects_level)
        self.objs_len = len(self.objs)

        self.sound_objs = (self.sound_level, self.effects_level)

    def _update_colors(self):
        self.objs[self._selected_obj].col = self._selected_obj_col

        if self._selected_obj == 0:
            self.objs[self._selected_obj + 1].col = self._nonselected_obj_col
        elif self._selected_obj == self.objs_len - 1:
            self.objs[self._selected_obj - 1].col = self._nonselected_obj_col
        else:
            self.objs[self._selected_obj + 1].col = self._nonselected_obj_col
            self.objs[self._selected_obj - 1].col = self._nonselected_obj_col

    def _update_sound(self, game_obj):
        sound_objs_names = 'music', 'effects'
        if self.objs[self._selected_obj] in self.sound_objs:
            game_obj.music.settings[sound_objs_names[self._selected_obj-1]] = str(self.objs[self._selected_obj].current_opt)
            game_obj.music.update()

    def _switch_option(self):
        if one_of_keys(px.KEY_UP, px.KEY_W):
            self._selected_obj -= 1
            if self._selected_obj < 0:
                self._selected_obj = 0

        if one_of_keys(px.KEY_DOWN, px.KEY_S):
            self._selected_obj += 1
            if self._selected_obj >= self.objs_len:
                self._selected_obj = self.objs_len - 1
        self._update_colors()

    def _select_option(self, game_obj):
        if one_of_keys(px.KEY_ESCAPE, px.KEY_SPACE, px.KEY_RETURN):
            if self.state == State.SELECTED:
                self.state = State.NONSELECTED
            else:
                self.state = State.SELECTED

            if self.state == State.NONSELECTED:
                self._update_sound(game_obj)

    def update(self, game_obj):
        self._select_option(game_obj)

        match self.state:
            case State.NONSELECTED:
                self._switch_option()
            case State.SELECTED:
                self.objs[self._selected_obj].process()

    def write_settings(self):
        objs_names = 'color_chooser', 'music', 'effects'
        settings = tuple(obj.current_opt for obj in self.objs)
        write_file('data.bin', dict(zip(objs_names, settings)))

    def draw(self):
        px.cls(14)
        for obj in self.objs:
            obj.draw()

