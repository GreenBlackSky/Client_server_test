"""Module contains methods for working with JSON configuration."""

from json import load as load_json
from sys import argv, stderr


def open_config(default_path):
    """Open and parse json file with configuration.

    Config file path should be passed as anonymous argument to app.
    Otherwise default path will be used.
    If any errors take place, print appropriate message.
    """
    if len(argv) > 1:
        conf_path = argv[1]
    else:
        conf_path = default_path

    try:
        with open(conf_path, 'r') as config_stream:
            config = load_json(config_stream)
    except OSError:
        print("Can't open config file", file=stderr)
        config = None
    except:
        print("Can't parse config file", file=stderr)
        config = None

    return config


def transform_config(config, config_must_have):
    """Cast values in config to appropriate types.

    config_must_have is to be a dict, containing names of required settings,
    and their types.
    Method also checks if config contains all reqired fields and nothing more.
    """
    for setting_name, setting_type in config_must_have.items():
        if set(config) - set(config_must_have):
            print("Excess values in config", file=stderr)
            return False
        if setting_name not in config:
            print("Incomplete config", file=stderr)
            return False
        else:
            try:
                config[setting_name] = setting_type(config[setting_name])
            except:
                print(setting_name, "is of incorrect type", file=stderr)
                return False
    return True

# TODO Make transforme_config recursive
