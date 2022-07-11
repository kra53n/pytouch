import pickle

import pyxel as px

from constants import DATA_PATH
from data import load_file


class Music:
    def __init__(self):
        self.settings = self.load_settings()
        self.sounds = {
            'music': {'id': 'music', 'play': True, 'ch': 0, 'snd': 0},
            'user_reach': {'id': 'effects', 'play': False, 'ch': 1, 'snd': 1},
            'user_missed': {'id': 'effects', 'play': False, 'ch': 1, 'snd': 2},
        }

        self.update()

    def load_settings(self) -> dict:
        data = load_file('data.bin')
        if data:
            return data
        std_val = '7'
        return {'music': std_val, 'effects': std_val}
    
    def write_settings(self, data: dict, filename: str):
        if not DATA_PATH.is_dir():
            DATA_PATH.mkdir()
        (DATA_PATH / filename).write_bytes(pickle.dumps(data.update(self.settings)))

    def update(self):
        for snd in self.sounds.values():
            if snd['play']:
                px.sound(snd['ch']).set_volumes(self.settings[snd['id']])
                px.play(snd['ch'], snd['snd'], loop=True)

