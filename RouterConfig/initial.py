import os
import signal

from common.shell import api
from RouterConfig import logger


class InitialHandler(object):

    def __init__(self):
        self.execute_api = api.API(logger=logger)

    def initial(self):
        logger.info('Initialization Started.')
        self._initial()
        logger.info('Initialization Accomplished.')

    def _initial(self):
        """Initial the router."""
        self._remove_default_route()
        self._remove_route_config()
        self._remove_iptables_config()
        self._remove_tc_config()

    def _remove_default_route(self):
        """Initialize the route table."""
        default_route_info = self.execute_api.execute_and_return('ip route | grep default').split('\n')[:-1]
        for i in range(len(default_route_info)):
            self.execute_api.execute('ip route del default')
        logger.info('Initialization: default route has been done.')

    def _remove_iptables_config(self):
        """Initialize the iptables."""
        for table in ['raw', 'mangle', 'filter', 'nat']:
            self.execute_api.execute('iptables -t ' + table + ' -F')
        logger.info('Initialization: iptables has been done.')

    def _remove_tc_config(self):
        """Initialize the tc."""
        all_nic = self._get_all_nic()
        for nic in all_nic:
            if nic != 'lo':
                self.execute_api.execute('tc qdisc del dev ' + nic + ' root')
        logger.info('Initialization: tc has been done.')

    def _remove_route_config(self):
        """Initialize the quagga."""

        def _remove_processes(self, process_name_list):
            """Terminate specified quagga processes."""
            for process_name in process_name_list:
                pid = self._get_pid_by_name(process_name + ' -d')
                if pid is not None:
                    os.kill(pid, signal.SIGTERM)

        def _remove_configuration(process_name_list):
            """Remove quagga configuration files."""
            for process_name in process_name_list:
                configuration_path = '/usr/local/etc/' + process_name + '.conf'
                if os.path.exists(configuration_path):
                    os.remove(configuration_path)

        process_name_list = ['zebra', 'ripd', 'ospfd', 'bgpd']
        _remove_processes(self, process_name_list)
        _remove_configuration(process_name_list)

    def _get_all_nic(self):
        """Get all nics."""
        nic_list = self.execute_api.execute_and_return(
            'ip a | grep \'<\' | awk \'{print $2}\' | cut -d \':\' -f 1').split('\n')[:-1]
        return nic_list

    def _get_pid_by_name(self, pname):
        """
        Get process id by process name.
        :param pname: name of process
        :type str
        :return pid of process
        :type int or None
        """
        pid_list = self.execute_api.execute_and_return(
            'ps aux | grep \'' + pname + '\' | grep -v \'grep\' | awk \'{print $2}\'').split('\n')[:-1]
        try:
            if pid_list:
                return int(pid_list[0])
            else:
                return None
        except Exception:
            return None
