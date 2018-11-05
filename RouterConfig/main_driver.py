from RouterConfig.common import schema as schemautils
from driver import Driver
from RouterConfig.route_config.route import RouteConfigDriver
from RouterConfig.data_filter.filter import DataFilterDriver
from RouterConfig.congestion_control.controller import CongestionControlDriver
from RouterConfig import logger
import schemas


class MainDriver(Driver):

    fields = [
        'route_config',
        'data_filter',
        'congestion_control',
        'priority_strategy'
    ]

    def __init__(self):
        self.sub_drivers = []

    @classmethod
    @schemautils.validate_schema(schemas.main_schema, logger=logger)
    def create_driver(cls, body):
        """create main driver and all sub drivers"""
        driver = cls()
        driver._create_sub_drivers(body)
        return driver

    def parse(self):
        """let all sub drivers to parse the configuration"""
        for sub_driver in self.sub_drivers:
            sub_driver.parse()

    def apply(self):
        """let all sub drivers to apply the configuration"""
        for sub_driver in self.sub_drivers:
            sub_driver.apply()

    def _create_sub_drivers(self, json_data):
        """create all sub drivers which should be used"""
        for field in self.fields:
            if field in json_data:
                config_data = json_data.get(field)
                if field == 'route_config':
                    self.sub_drivers.append(RouteConfigDriver.create_driver(body=config_data))
                elif field == 'data_filter':
                    self.sub_drivers.append(DataFilterDriver.create_driver(config_data))
                elif field == 'congestion_control':
                    self.sub_drivers.append(CongestionControlDriver.create_driver(config_data))
                elif field == 'priority_strategy':
                    pass
