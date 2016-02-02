import os
import sys
import logging
import logging.handlers
from metayaml import read

logger = None
conf = None

ENV_VARIABLES_PREFIX = 'TRUSY_'


def get_environment_params(conf, env2conf):
    """ Update configuration parameters with values from environment variables.
    """
    for k, v in env2conf.iteritems():
        path = v.split('.')
        container = reduce(lambda d, key: d.get(key), path[:-1], conf)
        print("Containder:%s" % container)
        new_value = os.environ.get('{}{}'.format(ENV_VARIABLES_PREFIX, k))
        if new_value:
            print("\tNew value:%s" % new_value)
            try:
                container[path[-1]] = new_value
            except TypeError:
                return False
    return True


def get_logger():
    global logger
    if not logger:
        logger = logging.getLogger(__package__)
        log_file = get_conf()['logging']['log_file']
        if log_file:
            # Add the log message handler to the logger
            max_bytes = int(get_conf()['logging']['max_bytes'])
            backup_count = int(get_conf()['logging']['backup_count'])
            ch = logging.handlers.RotatingFileHandler(log_file,
                                                      maxBytes=max_bytes,
                                                      backupCount=backup_count)
        else:
            ch = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - '
                                      '%(levelname)s - '
                                      '%(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)
        logger.setLevel(get_conf()['logging']['log_level'])
    return logger


def init_conf(local_conf=''):
    global conf
    global logger
    if not conf:
        configs = ["./trusty.yaml"]
        local_conf = local_conf or os.environ.get("LOCAL_CONF", None)
        if local_conf:
            configs.append(local_conf)
        conf = read(configs)
    if not logger:
        logger = get_logger()
    if not get_environment_params(conf, environment2configuration):
        sys.exit(1)
    return conf, logger


def get_conf():
    global conf
    if not conf:
        conf = init_conf()
    return conf

environment2configuration = {
    'LOG_LEVEL': 'common.log_level',
    'LOG_FILE': 'common.log_file',
}
