import os
import subprocess
import six


class API(object):

    def __init__(self, logger=None):
        self.logger = logger

    def execute(self, cmd):
        ret = os.system(cmd)
        if ret != 0:
            if self.logger is not None:
                self.logger.debug('Command: \'' + cmd + '\' is illegal.', exc_info=True)
            return False
        else:
            if self.logger is not None:
                self.logger.debug('Command: \'' + cmd + '\' has been applied.', exc_info=True)
            return True

    def execute_and_return(self, cmd):
        if six.PY2:
            ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0]
        else:
            ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).communicate()[0].decode()

        self.logger.debug('Command: \'' + cmd + '\' has been applied and return the following: \'' + ret + '\'.')
        return ret
