# encoding: utf-8
import re
import json
import requests
from alert.init_logger import alert_logger

def fetch_stock(stock_no):
    """
    根据股票代码去获取对应的点数及涨跌幅
    :param stock_no:
    :return:
    """
    resp = requests.get('http://api.money.126.net/data/feed/{0}'.format(stock_no))
    if resp.status_code == 200:
        pattern = re.compile('[(](.*)[)]', re.S)
        if type(resp.content) is bytes:
            resp_content = resp.content.decode('utf-8')
        else:
            resp_content = resp.content
        api_result = json.loads(re.findall(pattern, resp_content)[0])
        price = api_result[stock_no]['price']
        percent = api_result[stock_no]['percent']
        return price, percent * 100
    else:
        alert_logger.error("调用网易接口错误，请检查！")


if __name__ == '__main__':
    print(fetch_stock('0000001'))
    print(fetch_stock('1399001'))