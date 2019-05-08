from RouterConfig.driver import Driver
from RouterConfig.common.shell.api import API
from RouterConfig.data_filter.object import DataFilterParams
from RouterConfig.data_filter import logger


class DataFilterDriver(Driver):

    def __init__(self, json_data):
        self.data_filter_params_objs = [DataFilterParams()._from_json(body=k)
                                        for k in json_data
                                        if json_data is not None and len(json_data) > 0]
        self.execute_cmds = None
        self.execute_cmd_api = API(logger=logger)

    @classmethod
    def create_driver(cls, json_data):
        return cls(json_data)

    def parse(self):
        """parse the configuration to command"""
        self.execute_cmds = [data_filter_params_obj._to_iptables_cmd()
                             for data_filter_params_obj in self.data_filter_params_objs]

    def apply(self):
        """use api to apply the command"""
        logger.info("Start configuration of data filtering.")
        for execute_cmd in self.execute_cmds:
            if execute_cmd != '':
                self.execute_cmd_api.execute(execute_cmd)
        logger.info("Finish configuration of data filtering.")
