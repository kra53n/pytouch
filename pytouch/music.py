import pickle
import itertools

import pyxel as px

from constants import DATA_PATH
from settings import load_data


from pprint import pprint

class Music:
    def __init__(self):
        self.settings = load_data()
        self.sounds = {
            'music': {
                'music': {'loop': True, 'ch': 0, 'snd': 0},
            },
            'effects': {
                'user_reach': {'loop': False, 'ch': 1, 'snd': 1},
                'user_missed': {'loop': False, 'ch': 1, 'snd': 2},
            }
        }

        self.update(skip=('effects',))

    def write_settings(self, data: dict, filename: str):
        if not DATA_PATH.is_dir():
            DATA_PATH.mkdir()
        (DATA_PATH / filename).write_bytes(pickle.dumps(data.update(self.settings)))

    def play(self, user_snd_name):
        snds = tuple(itertools.chain.from_iterable(i.items() for i in self.sounds.values()))
        for snd_name, snd_data in snds:
            if user_snd_name == snd_name:
                px.play(snd_data['ch'], snd_data['snd'])

    def update(self, skip):
        for music_group, music_group_vals in self.sounds.items():
            if music_group in skip:
                continue
            for snd in music_group_vals.values():
                px.sound(snd['ch']).set_volumes(str(self.settings[music_group]))
                px.play(snd['ch'], snd['snd'], loop=snd['loop'])

