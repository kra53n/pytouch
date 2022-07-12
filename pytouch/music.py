import pickle

import pyxel as px

from constants import DATA_PATH
from settings import load_data


class Music:
    def __init__(self):
        self.settings = load_data()
        self.sounds = {
            'music': {
                'music': {'play': True, 'ch': 0, 'snd': 0},
            },
            'effects': {
                'user_reach': {'play': False, 'ch': 1, 'snd': 1},
                'user_missed': {'play': False, 'ch': 1, 'snd': 2},
            }
        }

        self.update()

    def write_settings(self, data: dict, filename: str):
        if not DATA_PATH.is_dir():
            DATA_PATH.mkdir()
        (DATA_PATH / filename).write_bytes(pickle.dumps(data.update(self.settings)))

    def update(self):
        for music_group in self.sounds.values():
            for snd_name, snd in music_group.items():
                if snd['play']:
                    px.sound(snd['ch']).set_volumes(str(self.settings[snd_name]))
                    px.play(snd['ch'], snd['snd'], loop=True)

