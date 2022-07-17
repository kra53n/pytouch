from constants import DATA_PATH
import pickle


def load_file(filename):
    path = DATA_PATH / filename
    if not path.exists():
        return ''
    return pickle.loads(path.read_bytes())


def write_file(filename: str, data):
    if not DATA_PATH.is_dir():
        DATA_PATH.mkdir()
    (DATA_PATH / filename).write_bytes(pickle.dumps(data))


def load_data():
    data = load_file('data.bin')
    default = {'score': 0, 'color_chooser': 0, 'music': 2, 'effects': 7}
    if isinstance(data, dict):
        data_keys = data.keys()
        for default_key, default_val in default.items():
            if default_key not in data_keys:
                data[default_key] = default_val
        return data
    return default
