import os
import logging
import logging.config

logger = logging.getLogger()
log_file = lambda x: os.path.abspath(__file__).replace("monk/log.py", "config/{}".format(x))

logging.config.fileConfig(
    log_file(os.environ.get("MONK_LOGGING", "log.cfg")))


if bool(os.environ.get("MONK_TEST", False)):
    logging.disable(logging.CRITICAL)
