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