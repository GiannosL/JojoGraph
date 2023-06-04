import yaml
from source.utilities.util_functions import validate_path


def parse_configuration(filename):
    """
    parse configuration file
    """
    config_file = validate_path(filename=filename)

    #
    with open(config_file, 'r') as stream:
        return yaml.safe_load(stream)
