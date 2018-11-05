from RouterConfig.driver import Driver
from RouterConfig.common.shell.api import API
from RouterConfig.speed_limit.object import SpeedLimitParams
from RouterConfig.speed_limit import logger


class SpeedLimitDriver(Driver):

    def __init__(self, json_data):
        self.speed_limit_params_objs = [SpeedLimitParams()._from_json(body=k)
                                       for k in json_data
                                       if json_data is not None and len(json_data) > 0]
        self.execute_cmds_list = None
        self.execute_cmd_api = API(logger=logger)

    @classmethod
    def create_driver(cls, json_data):
        return cls(json_data)

    def parse(self):
        """parse the configuration to command"""
        self.execute_cmds_list = [speed_limit_params_obj._to_tc_cmds()
                             for speed_limit_params_obj in self.speed_limit_params_objs]

    def apply(self):
        """use api to apply the command"""
        for execute_cmds in self.execute_cmds_list:
            for execute_cmd in execute_cmds:
                if execute_cmds != '':
                    self.execute_cmd_api.execute(execute_cmd)
