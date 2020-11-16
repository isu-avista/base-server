import yaml


def save(map, file):
    """ """
    with open(file, 'w') as f:
        yaml.dump(map, f)


def load(file):
    """ """
    with open(file, 'r') as f:
        return yaml.load(f, Loader=yaml.FullLoader)
