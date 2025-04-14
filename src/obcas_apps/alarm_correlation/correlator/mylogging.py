import logging
import os

logging.info('Alarm Correlation Application Starts')

def get_logger():
    DEFAULT_LOG_LEVEL = "DEBUG"
    log_level = os.environ.get('LOG_LEVEL', DEFAULT_LOG_LEVEL)
    logger = logging.getLogger('AlarmCorrelation')
    logger.setLevel(logging.getLevelName(log_level))
    return logger