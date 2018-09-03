import logging
logger = logging.getLogger('flask_monitor')
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
file_hander = logging.FileHandler('flask_monitor.log')
file_hander.setFormatter(formatter)
file_hander.setLevel(logging.DEBUG)
logger.addHandler(file_hander)
