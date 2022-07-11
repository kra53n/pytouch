from constants import DATA_PATH
import pickle


def load_file(filename):
    path = DATA_PATH / filename
    if not path.exists():
        return ''
    return pickle.loads(path.read_bytes())
