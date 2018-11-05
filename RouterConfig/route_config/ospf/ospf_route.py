from RouterConfig.common import schema as schemautils
from RouterConfig.common.shell.api import API as execute_cmd_api
from RouterConfig.driver import Driver
from RouterConfig.route_config import logger
import schemas


class OspfRouteConfigDriver(Driver):

    ospf_config_file = '/usr/local/etc/ospfd.conf'
    execute_cmd_api = execute_cmd_api(logger=logger)

    def __init__(self, json_data, router_id):
        self.config_dict = json_data
        self.router_id = router_id
        self.is_configured = False

    @classmethod
    @schemautils.validate_schema(schemas.ospf_route_config_schema, logger=logger)
    def create_driver(cls, body, router_id):
        return cls(body, router_id)

    def parse(self):
        if len(self.config_dict) > 0:
            ospf_conf = self.config_dict
            res = "hostname ospfd\npassword zebra\nrouter ospf\nospf router-id " + self.router_id + "\nlog-adjacency-changes\n"
            for ele in ospf_conf.get("networks"):
                res = res + "network " + ele.get("network") + " area " + str(ele.get("area")) + "\n"
            for ele in ospf_conf.get("others"):
                res = res + ele + "\n"
            with open(self.ospf_config_file, 'w') as f:
                f.write(res)
            self.is_configured = True
            logger.info('OSPF configuration has been parsed.')

    def apply(self):
        if self.execute_cmd_api.execute('ospfd -d'):
            logger.info('OSPF thread has been turned on.')
        else:
            logger.info('Fail to start OSPF thread.')

    @classmethod
    def parse_and_apply_default_config(cls, router_id):
        """parse the default configuration"""
        res = "hostname ospfd\npassword zebra\nrouter ospf\nospf router-id " + \
              router_id + "\nlog-adjacency-changes\nnetwork 0.0.0.0/0 area 0\n"
        with open(cls.ospf_config_file, 'w') as f:
            f.write(res)
        logger.info('OSPF default configuration has been parsed.')

        if cls.execute_cmd_api.execute('ospfd -d'):
            logger.info('Default OSPF thread has been turned on.')
        else:
            logger.info('Fail to start default OSPF thread.')
