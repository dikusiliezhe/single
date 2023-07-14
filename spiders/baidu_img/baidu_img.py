# -*- coding: utf-8 -*-
import json
import os
import sys
import traceback

import boto3

sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *


redis_name = "search_engine"


class BaiduImgSpider(Manager):
    name = 'baidu_img'
    custom_settings = {
        # 'retry_http_codes': [202, 412],
        'Waiting_time': 10,
        'IS_PROXY': True,
        'IS_SAMEIP': False,
        'UA_PROXY': True,
        # 'X_MAX_PRIORITY': 15,
        # 'max_request': 1,
        # 'PREFETCH_COUNT': 50
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36",
        }

        # self.params = {"keywords":["logo"],"total":"500","engine_type":"1"}
        self.params = json.loads(self.params)

    def start_requests(self):
        self.set_redis_value(redis_name, '1', json.dumps({'keywords':self.params['keywords'], 'engine_type':[1]}, ensure_ascii=False))
        self.set_redis_status(redis_name, '爬虫运行中')
        for parms in self.params['keywords']:
            url = "https://image.baidu.com/search/acjson?tn=resultjson_com&logid=8709288774945242143&ipn=rj&ct=201326592&fp=result&word={}&queryWord={}&cl=2&lm=-1&ie=utf-8&oe=utf-8&st=-1&face=0&istype=2&nc=1&pn=0&rn=30".format(parms, parms)
            yield MyRequests(url=url, headers=self.header, callback=self.get_pages, level=1, meta={'parms': parms})

    def get_pages(self, response):
        json_data = json.loads(response.text)
        total = int(json_data.get('displayNum'))
        if self.params.get('total'):
            total = min(total, int(self.params['total']))
        pages = int(total / 30) + 1
        for page in range(pages):
        # for page in range(1):
            url = response.url.replace('&pn=0', '&pn={}'.format(page))
            yield MyRequests(url=url, headers=self.header, callback=self.parse, level=2,
                             meta={'parms': response.meta.get('parms')})

    def parse(self, response):
        textt = response.text.encode('utf-8').decode("unicode_escape")
        try:
            json_data = json.loads(textt)
        except:
            json_data = json.loads(response.text)
            # total = json_data.get('displayNum')
        data_list = json_data.get('data')
        for data in data_list:
            if data:
                baidu_url = data.get('replaceUrl')[0].get('ObjURL')
                source_url = data.get('replaceUrl')[0].get('FromUrl')
                # self.prints({'baidu_url': baidu_url, 'source_url': source_url})
                yield MyRequests(url=baidu_url, headers=self.header, callback=self.parse_img, level=3,is_file=True, verify_ssl=False, meta={'parms': response.meta.get('parms')})


    def parse_img(self, response):
        file_path = self.oss_push_img(data=response.content, url=response.url, suffix='jpg', file_path='img/baidu/')
        print(file_path)


    def set_redis_status(self, redis_name, status):
        value = self.get_redis_value(redis_name, '1')
        value = json.loads(value)
        value['status'] = status
        self.set_redis_value(redis_name, '1', json.dumps(value, ensure_ascii=False))


if __name__ == '__main__':
    start_run = BaiduImgSpider()
    start_run.run()
    # start_run.set_redis_status(redis_name, '爬虫已结束')
