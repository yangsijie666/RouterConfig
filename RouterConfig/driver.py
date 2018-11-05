class Driver(object):

    def create_driver(self, *args, **kwargs):
        """create driver"""
        raise NotImplementedError()

    def parse(self, *args, **kwargs):
        """parse the configuration"""
        raise NotImplementedError()

    def apply(self, *args, **kwargs):
        """apply the configuration"""
        raise NotImplementedError()
