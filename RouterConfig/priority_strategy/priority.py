from RouterConfig.driver import Driver
from RouterConfig.common.shell.api import API
from RouterConfig.priority_strategy.object import PriorityStrategyParams
from RouterConfig.priority_strategy import logger


class PriorityStrategyDriver(Driver):

    def __init__(self, json_data):
        self.priority_strategy_params_objs = [PriorityStrategyParams()._from_json(body=k)
                                              for k in json_data
                                              if json_data is not None and len(json_data) > 0]
        self.execute_cmds_list = None
        self.execute_cmd_api = API(logger=logger)

    @classmethod
    def create_driver(cls, json_data):
        return cls(json_data)

    def parse(self):
        """parse the configuration to command"""
        self.execute_cmds_list = []
        mark_number = 1
        for priority_strategy_params_obj in self.priority_strategy_params_objs:
            self.execute_cmds_list.append(priority_strategy_params_obj._to_iptables_and_tc_cmds(mark_number))
            mark_number += 1

    def apply(self):
        """use api to apply the command"""
        for execute_cmds in self.execute_cmds_list:
            for execute_cmd in execute_cmds:
                if execute_cmds != '':
                    self.execute_cmd_api.execute(execute_cmd)
