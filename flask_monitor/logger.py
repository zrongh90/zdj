import logging
from logging.handlers import RotatingFileHandler
logger = logging.getLogger('flask_monitor')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
file_hander = RotatingFileHandler(filename='flask_monitor.log', maxBytes=1024*1024, backupCount=5)
file_hander.setFormatter(formatter)
file_hander.setLevel(logging.DEBUG)
logger.addHandler(file_hander)
