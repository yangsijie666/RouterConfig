import os

from RouterConfig.common import schema as schemautils
from RouterConfig.driver import Driver
from zebra.api import API as zebra_api
from static.static_route import StaticRouteConfigDriver
from rip.rip_route import RipRouteConfigDriver
from ospf.ospf_route import OspfRouteConfigDriver
from bgp.bgp_route import BgpRouteConfigDriver
from RouterConfig.route_config import logger
import schemas


class RouteConfigDriver(Driver):

    fields = [
        'static',
        'rip',
        'ospf',
        'bgp'
    ]

    def __init__(self):
        self.router_id = self._generate_router_id()
        self.sub_drivers = []
        self.zebra_api = zebra_api()
        self.zebra_api.init_zebra()

    @classmethod
    @schemautils.validate_schema(schemas.route_config_schema, logger=logger)
    def create_driver(cls, body):
        """create driver"""
        driver = cls()
        driver._create_sub_drivers(body)
        return driver

    def parse(self):
        """parse the configuration to all sub drivers"""
        _sub_drivers = []
        for driver in self.sub_drivers:
            driver.parse()
            if driver.is_configured:
                _sub_drivers.append(driver)
        self.sub_drivers = _sub_drivers

    def apply(self):
        """apply the configuration to all the sub drivers"""
        self.zebra_api.start_zebra()
        if len(self.sub_drivers) > 0:
            for driver in self.sub_drivers:
                driver.apply()
        else:
            self.parse_and_apply_default_config()

    def parse_and_apply_default_config(self):
        """parse the default configuration"""
        default_driver = OspfRouteConfigDriver
        default_driver.parse_and_apply_default_config(self.router_id)

    def _create_sub_drivers(self, json_data):
        for field in self.fields:
            if field in json_data:
                config_data = json_data.get(field)
                if field == 'static':
                    self.sub_drivers.append(StaticRouteConfigDriver.create_driver(body=config_data))
                elif field == 'rip':
                    self.sub_drivers.append(RipRouteConfigDriver.create_driver(body=config_data))
                elif field == 'ospf':
                    self.sub_drivers.append(OspfRouteConfigDriver.create_driver(body=config_data, router_id=self.router_id))
                elif field == 'bgp':
                    self.sub_drivers.append(BgpRouteConfigDriver.create_driver(body=config_data, router_id=self.router_id))

    @staticmethod
    def _generate_router_id():
        eth = os.popen("ip address | grep 'inet '| grep global")
        eth = eth.read().split('\n')[:-1]
        eth_ip = {}
        ch3 = lambda x: sum([256 ** j * int(i) for j, i in enumerate(x.split('.')[::-1])])
        for ele in eth:
            ip = ele.split()[1]
            ip = ip.split('/')[0]
            eth_ip[ip] = ch3(ip)
        router_id = max(eth_ip, key=eth_ip.get)
        return router_id
