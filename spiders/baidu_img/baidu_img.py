# -*- coding: utf-8 -*-
import os
import sys

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *


class BaiduImgSpider(Manager):
    name = 'baidu_img'
    custom_settings = {
        # 'retry_http_codes': [202, 412],
        'Waiting_time': 100,
        'IS_PROXY': True,
        'IS_SAMEIP': False,
        'UA_PROXY': False,
        # 'X_MAX_PRIORITY': 15,
        # 'max_request': 1,
        # 'PREFETCH_COUNT': 50
    }
    # print(custom_settings)
    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
        }

        self.total = 0


    def start_requests(self):
        print(self.params)
        url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8709288774945242143&ipn=rj&ct=201326592&fp=result&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&face=0&istype=2&nc=1&pn=120&rn=30&gsm=78".format(self.params, self.params)
        yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        self.total+=1
        json_data = json.loads(response.text)
        total = json_data.get('displayNum')
        data_list = json_data.get('data')
        for data in data_list:
            if data:
                try:
                    baidu_url = data.get('replaceUrl')[0].get('ObjURL')
                    source_url = data.get('replaceUrl')[0].get('FromUrl')
                    print(baidu_url, source_url)
                except:
                    print(data)

if __name__ == '__main__':
    start_run = BaiduImgSpider()
    start_run.run()
