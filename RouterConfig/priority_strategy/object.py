import subprocess

from RouterConfig.common import schema as schemautils
from RouterConfig.priority_strategy import schemas
from RouterConfig.priority_strategy import logger
from RouterConfig.common.shell.api import API


class PriorityStrategyParams(object):

    fields = [
        'source_mac',
        'ip_address',
        'port',
        'protocol',
        'interface',
        'priority'
    ]

    execute_cmd_api = API(logger=logger)

    def as_dict(self):
        """transform the object to dict"""
        return {
            k: getattr(self, k)
            for k in self.fields
            if self.obj_attr_is_set(k)
        }

    @schemautils.validate_schema(schemas.priority_strategy_schema, logger=logger)
    def _from_json(self, body):
        """
        transform from the json data to object
        :param body: the json data
        :type dict
        :return:
        """
        for field in self.fields:
            body_field_val = body.get(field, None)
            if body_field_val is None or len(body_field_val) == 0:
                continue
            setattr(self, field, body_field_val)
        return self

    def obj_attr_is_set(self, attr):
        """check if the object has the attribute"""
        try:
            getattr(self, attr)
        except AttributeError:
            return False
        else:
            return True

    def _to_iptables_and_tc_cmds(self, mark_number):
        """
        transform from the PriorityStrategyParams object to iptables and tc commands
        :param mark_number: number which should be used to mark the data
        :type int
        :return: command of tc and iptables
        :type: list
        """
        cmds = []
        cmds.append(self._to_iptables_cmd(mark_number))
        cmds.extend(self._to_tc_cmds(mark_number))
        return cmds

    def _to_iptables_cmd(self, mark_number):
        """
        transform from the PriorityStrategyParams object to iptables command.
        :param mark_number: number which should be used to mark the data
        :return: command of iptables
        :type str
        """
        cmd = 'iptables '
        cmd_table = '-t raw -A PREROUTING '
        cmd_params = ''
        cmd_act = '-j MARK --set-mark ' + str(mark_number)

        if self.obj_attr_is_set('source_mac'):
            mac_params = getattr(self, 'source_mac')
            cmd_params += '-m mac --mac-source ' + mac_params + ' '

        if self.obj_attr_is_set('port'):
            if self.obj_attr_is_set('protocol'):
                if getattr(self, 'protocol') == 'all':
                    logger.error('\'port\' can not be specified while \'protocol\' is set to \'all\'.', exc_info=True)
                    return ''
            else:
                logger.error('\'port\' can not be specified while \'protocol\' is not set.', exc_info=True)
                return ''
            pro = getattr(self, 'protocol')
            port_params = getattr(self, 'port')
            if port_params.get('src', None) is not None and len(port_params.get('src')) > 0:
                cmd_params += '-m ' + pro + ' --sport ' + port_params.get('src') + ' '
            if port_params.get('dst', None) is not None and len(port_params.get('dst')) > 0:
                cmd_params += '-m ' + pro + ' --dport ' + port_params.get('dst') + ' '

        if self.obj_attr_is_set('protocol'):
            protocol_params = getattr(self, 'protocol')
            cmd_params += '-p ' + protocol_params + ' '

        if self.obj_attr_is_set('ip_address'):
            address_params = getattr(self, 'ip_address')
            if address_params.get('src', None) is not None and len(address_params.get('src')) > 0:
                cmd_params += '-s '
                for src_address in address_params.get('src'):
                    cmd_params += src_address + ','
                cmd_params = cmd_params.rsplit(',', 1)[0] + ' '
            if address_params.get('dst', None) is not None and len(address_params.get('dst')) > 0:
                cmd_params += '-d '
                for dst_address in address_params.get('dst'):
                    cmd_params += dst_address + ','
                cmd_params = cmd_params.rsplit(',', 1)[0] + ' '

        cmd = cmd + cmd_table + cmd_params + cmd_act
        return cmd

    def _to_tc_cmds(self, mark_number):
        """
        transform from the PriorityStrategyParams object to tc commands
        :param mark_number: number which should be used to mark the data
        :type int
        :return: commands of tc
        :type list
        """
        cmds = []

        prio_handle = self._get_prio_info()
        if prio_handle is not None:
            cmds.append(self._generate_prio_filter(prio_handle, mark_number))
        else:
            htb_info = self._get_htb_info()
            if htb_info is not None:
                htb_handle, htb_classid = htb_info
                prio_handle = str(int(htb_handle) + 1)

                # create a qdisc prio first before generate filters
                self.apply_qdisc_prio(htb_classid, prio_handle)
                cmds.append(self._generate_prio_filter(prio_handle, mark_number))
            else:
                self.init_qdisc()
                # create a qdisc prio first before generate filters
                self.apply_qdisc_prio('root', '1')
                cmds.append(self._generate_prio_filter('1', mark_number))

        return cmds

    def init_qdisc(self):
        """
        Delete all qdisc on root.
        :return:
        """
        cmd = 'tc qdisc del dev {} root'.format(self.interface)
        self.execute_cmd_api.execute(cmd)

    def apply_qdisc_prio(self, parent_handle, handle):
        """
        Configure qdisc for the priority queue.
        :param parent_handle: parent's handle (such as 1:1)
        :param handle: handle of self (such as 2)
        :return:
        """
        cmd = 'tc qdisc add dev {} parent {} handle {}: prio'\
            .format(self.interface, parent_handle, handle)
        self.execute_cmd_api.execute(cmd)

    def _generate_prio_filter(self, parent_handle, handle):
        """
        Generate filters for the priority queue.
        :param parent_handle: parent's handle (such as 1)
        :param handle: handle of self (such as 2)
        :return:
        """
        priority = self._get_filter_priority()
        cmd = 'tc filter add dev {} prio 8 parent {}: handle {} fw flowid {}:{}'\
            .format(self.interface, parent_handle, handle, parent_handle, priority)
        return cmd

    def _get_filter_priority(self):
        """
        Get priority based on the configuration file.
        :return:
        """
        prio_str = getattr(self, 'priority')
        if prio_str == 'low':
            return '3'
        elif prio_str == 'high':
            return '1'
        else:
            return '2'

    def _get_prio_info(self):
        """
        Get the handle of the existing prio qdisc.
        :return: handle of prio qdisc (such as 2)
        :type str
        """
        ret = subprocess.Popen('tc -s qdisc show dev %s | grep " prio " | cut -d " " -f 3' % self.interface,
                               shell=True, stdout=subprocess.PIPE).communicate()[0].strip(':\n')
        if ret == '':
            return None
        else:
            prio_handle = ret
            return prio_handle

    def _get_htb_info(self):
        """
        Get the handle and classid of the existing htb qdisc.
        :return: handle(such as 1) and classid(such as 1:1)
        :type str
        """
        ret = subprocess.Popen('tc -s qdisc show dev %s | grep " htb " | cut -d " " -f 3' % self.interface,
                               shell=True, stdout=subprocess.PIPE).communicate()[0].strip(':\n')
        if ret == '':
            return None
        else:
            htb_handle = ret
            ret = subprocess.Popen('tc -s class show dev %s | grep " htb " | cut -d " " -f 3' % self.interface,
                               shell=True, stdout=subprocess.PIPE).communicate()[0]
            if ret == '':
                return None
            else:
                htb_classid = ret
                return (htb_handle, htb_classid)
