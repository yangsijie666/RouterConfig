from RouterConfig.common import schema as schemautils
from RouterConfig.congestion_control import schemas
from RouterConfig.congestion_control import logger


class CongestionControlParams(object):

    fields = [
        'nic',
        'speed'
    ]

    def as_dict(self):
        """transform the object to dict"""
        return {
            k: getattr(self, k)
            for k in self.fields
            if self.obj_attr_is_set(k)
        }

    @schemautils.validate_schema(schemas.congestion_control_schema, logger=logger)
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

    def _to_tc_cmds(self):
        """
        transform from the data_filter_schema to tc commands
        :return: commands of tc
        :type: list
        """
        cmds = []
        cmds.append(self._init_tc_config())

        cmds.append('tc qdisc add dev {} root handle 1: htb default 1 r2q 0'.format(self.nic))
        cmds.append('tc class add dev {} classid 1:1 htb rate {} ceil {}'.format(self.nic, self.speed, self.speed))
        return cmds

    def _init_tc_config(self):
        return 'tc qdisc del dev {} root'.format(self.nic)
