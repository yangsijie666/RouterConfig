import sys

sys.path.extend(['/RouterConfig'])  # the python file is put at /RouterConfig/RouterConfig/main.py

import load_file
from main_driver import MainDriver
from common.shell import api


def init_router():
    """The router should not have a default route by default."""
    execute_api = api.API()
    execute_api.execute('ip route del default')


def load_config(config_file_path):
    return load_file.load_config(config_file_path)


def main(config_file_path):
    init_router()

    driver = MainDriver.create_driver(body=load_config(config_file_path))
    driver.parse_and_apply()


if __name__ == '__main__':
    main('/root/config.json')
