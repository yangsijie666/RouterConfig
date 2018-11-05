from RouterConfig.common import schema as schemautils
from RouterConfig.common.shell.api import API as execute_cmd_api
from RouterConfig.driver import Driver
from RouterConfig.route_config import logger
import schemas


class BgpRouteConfigDriver(Driver):

    bgp_config_file = '/usr/local/etc/bgpd.conf'
    execute_cmd_api = execute_cmd_api(logger=logger)

    def __init__(self, json_data, router_id):
        self.config_dict = json_data
        self.router_id = router_id
        self.is_configured = False

    @classmethod
    @schemautils.validate_schema(schemas.bgp_route_config_schema, logger=logger)
    def create_driver(cls, body, router_id):
        return cls(body, router_id)

    def parse(self):
        if len(self.config_dict) != 0:
            bgp_conf = self.config_dict
            res = "hostname bgpd\npassword zebra\nrouter bgp "
            res = res + str(bgp_conf.get("as_num")) + "\nbgp router-id " + self.router_id + "\n"
            res += "bgp log-neighbor-changes\n"
            if 'network' in bgp_conf:
                for ele in bgp_conf.get("network"):
                    res = res + "network " + ele + "\n"
            if 'ebgp_neighbors' in bgp_conf:
                for ele in bgp_conf.get("ebgp_neighbors"):
                    res = res + "neighbor " + ele.get("neighbor_ip") + " remote-as " + str(
                        ele.get("neighbor_as")) + "\n"
            if 'ibgp_neighbors' in bgp_conf:
                for ele in bgp_conf.get("ibgp_neighbors"):
                    res = res + "neighbor " + ele + " remote-as " + str(
                        bgp_conf.get("as_num")) + "\nneighbor " + ele + " next-hop-self\n"
            if 'others' in bgp_conf:
                for ele in bgp_conf.get("others"):
                    res = res + ele + "\n"
            with open(self.bgp_config_file, 'w') as f:
                f.write(res)
            self.is_configured = True
            logger.info('BGP configuration has been parsed.')

    def apply(self):
        if self.execute_cmd_api.execute('bgpd -d'):
            logger.info('BGP thread has been turned on.')
        else:
            logger.info('Fail to start BGP thread.')
