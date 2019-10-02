import logging
import sys


logger = logging.getLogger('tanapol')
log_format = logging.Formatter('[%(levelname)s] %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(log_format)
logger.addHandler(stream_handler)


def set_log_level(v):
    verbosity = 0
    if v is not None:
        verbosity = v
        if verbosity > 2:
            print('Too much verbosity. Setting verbosity to -vv')
            verbosity = 2
    stream_handler.setLevel(logging.WARNING - logging.DEBUG * verbosity)


def handle_exception(exc_type, exc_value, exc_traceback, **kwargs):
    logger.error("Uncaught exception",
                 exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback, **kwargs)


sys.excepthook = handle_exception
