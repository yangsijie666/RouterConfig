from RouterConfig.common import schema as schemautils
from RouterConfig.common.shell.api import API as execute_cmd_api
from RouterConfig.driver import Driver
from RouterConfig.route_config import logger
from RouterConfig.route_config.zebra.api import API as zebra_api
import schemas


class StaticRouteConfigDriver(Driver):

    zebra_config_file = zebra_api.zebra_config_file
    execute_cmd_api = execute_cmd_api(logger=logger)

    def __init__(self, json_data):
        self.config_dict = json_data
        self.is_configured = False

    @classmethod
    @schemautils.validate_schema(schemas.static_route_config_schema, logger=logger)
    def create_driver(cls, body):
        return cls(body)

    def parse(self):
        if len(self.config_dict) > 0:
            res = ""
            for static_info in self.config_dict:
                if len(static_info) > 0:
                    next_hop_or_src_port = static_info.get('next_hop')
                    for dst_prefix in static_info.get('dst_prefix'):
                        cmd = 'ip route {0} {1}'.format(dst_prefix, next_hop_or_src_port)
                        res = res + cmd + '\n'
                        self.is_configured = True

            with open(self.zebra_config_file, 'a') as f:
                f.write(res)
            logger.info('Static Route configuration has been parsed.')

    def apply(self):
        if self.execute_cmd_api.execute('systemctl restart frr'):
            logger.info('Static Route thread has been turned on.')
        else:
            logger.error('Fail to start Zebra for Static Route thread.')
