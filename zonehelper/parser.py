import yaml


def get_hosts_info(path):
    return yaml.safe_load(open(path))
