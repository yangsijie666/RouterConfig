import os
import time
import signal
from multiprocessing import Process

from main_driver import MainDriver
from initial import InitialHandler
from load import LoadFileHandler
from common.shell import api
from RouterConfig import logger


class ConfigureHandler(object):

    def __init__(self, config_file_path):
        self.config_file_path = config_file_path
        self.load_file_handler = LoadFileHandler(self.config_file_path)
        self.execute_api = api.API(logger=logger)
        self.last_configure_process = None
        self.first_boot = True
        self.last_modified_time = None

    def configure(self):
        """Configure."""
        self._configure()

    def _configure(self):
        """Loop through the configuration file to see if it changes and start configure."""
        while True:
            config_file = None

            if self.first_boot:
                config_file = self.load_file_handler.load_config_file(first_load=True)
                self.first_boot = False
            else:
                if self._listen_file_modified():
                    config_file = self.load_file_handler.load_config_file(first_load=False)

            if config_file is not None:
                self._create_config_process(config_file)

            time.sleep(5)

    def _listen_file_modified(self):
        """Whether the listener file has been modified."""
        modified_time = os.stat(self.config_file_path).st_mtime
        if (self.last_modified_time is not None) and (modified_time == self.last_modified_time):
            return False
        else:
            self.last_modified_time = modified_time
            return True

    def _create_config_process(self, config_file):
        """Create subprocess to parse and apply the configuration."""
        # Before we create the new process, we must be sure
        # that the old process has been terminated.
        if (self.last_configure_process is not None) and \
                self._check_process_exists_by_pid(self.last_configure_process):
            os.kill(self.last_configure_process, sig=signal.SIGTERM)

        configure_process = ConfigureProcess(config_file)
        self.last_configure_process = configure_process.pid
        configure_process.start()

    def _check_process_exists_by_pid(self, pid):
        """
        Check if the process specified by pid exists.
        :param pid: process id of Process
        :return: True of False
        """
        res = self.execute_api.execute_and_return('ps aux | awk \'{print $2}\' | grep \'^' + str(pid) + '$\'').split(
            '\n')[:-1]
        if res:
            return True
        else:
            return False


class ConfigureProcess(Process):
    """Subprocess to parse and apply the configuration."""

    def __init__(self, config_file):
        super(ConfigureProcess, self).__init__()
        self.daemon = True
        self.initial_handler = InitialHandler()
        self.driver = MainDriver.create_driver(body=config_file)

    def run(self):
        self.initial_handler.initial()
        self.driver.parse_and_apply()
