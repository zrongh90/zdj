# encoding: utf-8
import logging
alert_logger = logging.getLogger()
alert_logger.setLevel(logging.DEBUG)
log_format = logging.Formatter("%(name)s-%(levelname)s-%(message)s")
log_handle = logging.FileHandler('alert.log')
log_handle.setFormatter(log_format)
alert_logger.addHandler(log_handle)