import sys
sys.path.extend(['/RouterConfig'])  # the python file is put at /RouterConfig/RouterConfig/main.py

from config import ConfigureHandler


def main(config_file_path):
    """Main process."""
    configure_handler = ConfigureHandler(config_file_path)
    configure_handler.configure()


if __name__ == '__main__':
    sys.exit(main('/root/config.json'))
