from RouterConfig.common.shell.api import API as execute_cmd_api
from RouterConfig.route_config import logger


class API(object):

    zebra_config_file = '/etc/frr/frr.conf'

    def __init__(self):
        self.execute_cmd_api = execute_cmd_api()

    @classmethod
    def init_zebra(cls):
        res = "hostname frr\n"
        with open(cls.zebra_config_file, 'a') as f:
            f.write(res)
        logger.info('Zebra has been initiated.')

    def start_zebra(self):
        if self.execute_cmd_api.execute('systemctl restart frr'):
            logger.info('Zebra thread has been turned on.')
        else:
            logger.info('Fail to start Zebra thread.')
