import yaml

config_filename = "config.yaml"


def get_config():
    with open(config_filename, "r") as fh:
        return yaml.safe_load(fh)
