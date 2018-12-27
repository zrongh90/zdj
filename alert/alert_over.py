# encoding: utf-8
import requests
from alert.init_logger import alert_logger
from alert.config import ALERT_OVER_RECEIVERS, ALERT_OVER_SOURCE, ALERT_OVER_URL


def alert_over(title, content):
    """
    通过alert_over的接口去进行提醒
    :param title: 消息标题
    :param content: 消息正文
    :return:
    """
    alert_logger.debug("init alert over api to send message")
    response_res = requests.post(
                            ALERT_OVER_URL,
                            data={
                                "source": ALERT_OVER_SOURCE,
                                "receiver": ALERT_OVER_RECEIVERS,
                                "title": title,
                                "content": content
                                }
                            )
    alert_logger.debug(response_res)