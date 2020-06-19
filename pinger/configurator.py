import yaml
from pathlib import Path
import os


def get_configuration(configuration_file):
    with open(Path(os.path.expanduser(configuration_file))) as f:
        conf = yaml.load(f, Loader=yaml.FullLoader)
    return conf
