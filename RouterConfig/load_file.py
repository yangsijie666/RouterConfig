import time
import os
import json
from collections import OrderedDict

from common.httpclient import HttpClient
from RouterConfig import logger


def load_config(local_config_path=None):

    new_dict = None

    # attempt to get config file from user data first
    use_user_data_flag = True
    try:
        logger.info('Try to get config file from user data.')
        user_data_url = 'http://169.254.169.254/latest/user-data'
        response = HttpClient(method='GET', url=user_data_url, timeout=10).process
        status_code = response.status_code
        if status_code != 200:
            logger.info('Get config file from user data failed.')
            use_user_data_flag = False
        else:
            logger.info('Get config file from user data successfully.')
            new_dict = response.json()
            return new_dict
    except:
        logger.info('Get config file from user data failed.')
        use_user_data_flag = False

    # try to get config file from local user data file
    if not use_user_data_flag:
        logger.info('Try to get config file from user data (from local file).')
        if os.path.exists('/dev/sr0'):
            # read config file from user data
            os.system('mount /dev/sr0 /mnt')
            if os.path.exists('/mnt/openstack/latest/user_data'):
                try:
                    with open('/mnt/openstack/latest/user_data', 'r') as f:
                        new_dict = json.load(f, object_pairs_hook=OrderedDict)
                    logger.info('Get config file from user data successfully (from local file).')
                    return new_dict
                except:
                    logger.info('Get config file from user data failed (from local file).')
                    use_user_data_flag = False
            os.system('umount /mnt')
        else:
            use_user_data_flag = False

    # try to get config file from local file
    if local_config_path is not None:
        if not use_user_data_flag:
            # read config file: /root/config.json
            logger.info('Try to get config file from local file.')
            while True:
                try:
                    with open(local_config_path, 'r') as f:
                        new_dict = json.load(f, object_pairs_hook=OrderedDict)
                    logger.info('Get config file from local file successfully.')
                    return new_dict
                except:
                    time.sleep(1)
                    continue
