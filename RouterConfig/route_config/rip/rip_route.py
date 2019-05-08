from RouterConfig.common import schema as schemautils
from RouterConfig.common.shell.api import API as execute_cmd_api
from RouterConfig.driver import Driver
from RouterConfig.route_config import logger
import schemas


class RipRouteConfigDriver(Driver):

    rip_config_file = '/usr/local/etc/ripd.conf'
    execute_cmd_api = execute_cmd_api(logger=logger)

    def __init__(self, json_data):
        self.config_dict = json_data
        self.is_configured = False

    @classmethod
    @schemautils.validate_schema(schemas.rip_route_config_schema, logger=logger)
    def create_driver(cls, body):
        return cls(body)

    def parse(self):
        if len(self.config_dict) > 0:
            rip_conf = self.config_dict
            res = "hostname zebra\npassword zebra\nrouter rip\n"
            # get rip version (default: version 2)
            rip_version = rip_conf.get("version", 2)
            res += 'version ' + str(rip_version) + '\n'
            # configure the network of rip
            if "networks" in rip_conf:
                for network in rip_conf.get("networks"):
                    res += "network " + network + "\n"
            # configure other rip configuration
            if 'others' in rip_conf:
                for other_config in rip_conf.get('others'):
                    res += other_config + '\n'
            # save the configuration
            with open(self.rip_config_file, 'w') as f:
                f.write(res)
            self.is_configured = True
            logger.info('RIP configuration has been parsed.')

    def apply(self):
        if self.execute_cmd_api.execute('ripd -d'):
            logger.info('RIP thread has been turned on.')
        else:
            logger.error('Fail to start RIP thread.')
