# encoding: utf-8
import requests
from bs4 import BeautifulSoup
from alert.alert_over import alert_over

MONEY_163 = "http://money.163.com/"


def get_163_news():
    """

    :return:
    """
    money_163_resp = requests.get(MONEY_163)
    if money_163_resp.status_code != 200:
        exit(1)
    money_163_bs4 = BeautifulSoup(money_163_resp.content, "html.parser")
    # news = []
    for nlist in money_163_bs4.find_all('ul', {'class','topnews_nlist'}):
        # for new in nlist.findAll('a'):
        #     print(new)
        for new in nlist.find_all(['h2', 'h3']):
            url = new.find('a').get('href')
            title = new.find('a').text
            # TODO: 正文内容摘要生成
            alert_over(title, title, url)
            # news.append({'url': url, 'title': title})
    # print(money_163_bs4.findAll('ul', {'class','topnews_nlist'})[0])
    # return news


if __name__ == "__main__":
    print(get_163_news())