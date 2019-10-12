import logging
import sys

from tanapol.argparse import args


logger = logging.getLogger('tanapol')
log_format = logging.Formatter('[%(levelname)s] %(message)s')
logger.setLevel(logging.DEBUG)

stream_handler = logging.StreamHandler(stream=sys.stdout)
stream_handler.setFormatter(log_format)
verbosity = min(2, args.v)
stream_handler.setLevel(logging.WARNING - logging.DEBUG * verbosity)
logger.addHandler(stream_handler)

logger.debug('test')


def handle_exception(exc_type, exc_value, exc_traceback, **kwargs):
    logger.error("Uncaught exception",
                 exc_info=(exc_type, exc_value, exc_traceback))
    sys.__excepthook__(exc_type, exc_value, exc_traceback, **kwargs)


sys.excepthook = handle_exception
