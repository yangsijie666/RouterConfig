from RouterConfig.common import schema as schemautils
from RouterConfig.data_filter import schemas
from RouterConfig.data_filter import logger


class DataFilterParams(object):

    fields = [
        'source_mac',
        'ip_address',
        'port',
        'protocol',
        'nic'
    ]

    def as_dict(self):
        """transform the object to dict"""
        return {
            k: getattr(self, k)
            for k in self.fields
            if self.obj_attr_is_set(k)
        }

    @schemautils.validate_schema(schemas.data_filter_schema, logger=logger)
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

    def _to_iptables_cmd(self):
        """
        transform from the data_filter_schema to iptables command
        :return: command of iptables
        :type: str
        """
        cmd = 'iptables '
        cmd_table = '-t raw -A PREROUTING '
        cmd_params = ''
        cmd_act = '-j DROP'

        if self.obj_attr_is_set('nic'):
            nic_params = getattr(self, 'nic')
            if self.obj_attr_is_set('source_mac'):
                if len(nic_params) == 2 or \
                        (len(nic_params) == 1 and nic_params.get('out', None) is not None):
                    logger.error('\'source_mac\' and \'nic out\' can not be specified together.', exc_info=True)
                    return ''
            if len(nic_params) == 2:
                cmd_table = '-t mangle -A FORWARD '
                cmd_params = '-i ' + nic_params.get('in') + ' -o ' + nic_params.get('out') + ' '
            elif len(nic_params) == 1:
                if nic_params.get('out', None) is not None:
                    cmd_table = '-t mangle -A POSTROUTING '
                    cmd_params = '-o ' + nic_params.get('out') + ' '
                else:
                    cmd_params = '-i ' + nic_params.get('in') + ' '

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
