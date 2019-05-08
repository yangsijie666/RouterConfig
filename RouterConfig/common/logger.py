import logging


class Logger(object):

    def __init__(self, log_file_name):
        self.log_file_name = log_file_name
        self.logger = logging.getLogger(log_file_name)
        self.init_logger()

    def init_logger(self):
        """initiate the logger"""
        self.logger.setLevel(logging.INFO)
        # define the log file location
        logfile = '/var/log/RouterConfig/' + self.log_file_name + '.log'
        fh = logging.FileHandler(logfile, mode='a')
        fh.setLevel(logging.DEBUG)
        # define the format of log
        formatter = logging.Formatter("%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

    @classmethod
    def create_logger(cls, log_file_name):
        """use this method to get logger"""
        return cls(log_file_name).logger
