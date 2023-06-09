# -*- coding: utf-8 -*-
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *

def get_ss(ss):
    js = ""
    fp1 = open('./a.js', encoding='utf-8')
    js += fp1.read()
    fp1.close()
    ctx2 = execjs.compile(js)
    return ctx2.call('encryptWithAES', ss)
class HongcanKaidianshixvSpider(Manager):
    name = 'hongcan_kaidianshixv'

    custom_settings = {
        'PREFETCH_COUNT': 10,
        'Waiting_time': 10000,
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }


    def start_requests(self):
        cursor = 0
        while True:
            # 使用HSCAN命令进行迭代
            cursor, hash_data = self.r.hscan("hongcan_data", cursor)

            # 处理获取到的hash字段和对应的值

            for field, value in hash_data.items():
                data = f'{{"brand_id":"{field}"}}&date={self.get_timestamp()}&version=2'
                data_str = get_ss(data)
                url = 'https://topm.canyin88.com/api/v2/analyse/getBrandStoresOpenClose?data={}'.format(data_str)
                name = json.loads(value).get('name')
                yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1, meta={'brand_id':field, 'name':name})
            # 如果cursor值为0，表示迭代完成，退出循环
            if cursor == 0:
                break

    def parse(self, response):
        data_list = json.loads(response.text).get('data')
        json_dict = {'brand_id':response.meta.get('brand_id'), 'brand_name':response.meta.get('name'),  'data':data_list}
        self.kafka_producer('boss.de_nine.spider.hongcanApp_stoneSourt', json_dict)


if __name__ == '__main__':
    start_run = HongcanKaidianshixvSpider()
    start_run.run()