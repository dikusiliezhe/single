# -*- coding: utf-8 -*-
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *


class HongcanCitySpider(Manager):
    name = 'hongcan_city'
    custom_settings = {
        'PREFETCH_COUNT': 10,
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        pages = 1607
        for page in range(1, pages):
            # for page in range(1, 2):
            data = f'{{"master_type":"0","second_type":"","city_id":"","province_id":"","order_by":"store_count","desc":"desc","pagesize":10,"page":{page},"keyword":"","top_bg":""}}&date={self.get_timestamp()}&version=2'
            data_str = self.get_ss(data)
            url = 'https://topm.canyin88.com/api/v2/brands/search?data={}'.format(data_str)
            yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        data_list = json.loads(response.text).get('data').get('data')
        for data in data_list:
            id = data.get('id')
            name = data.get('name')
            params = f'{{"brand_id":"{id}"}}&date={self.get_timestamp()}&version=2'
            data_str = self.get_ss(params)
            url = 'https://topm.canyin88.com/api/v2/analyse/getBrandStoreAreas?data={}'.format(data_str)
            yield MyRequests(url=url, headers=self.header, callback=self.get_detail, level=2, meta={'id':id, 'name':name})

    def get_detail(self, response):
        meta = response.meta
        data_list = json.loads(response.text).get('data')
        for data in data_list:
            dpcode = data.get('dpcode')
            params = f'{{"brand_id":"{meta.get("id")}","city_id":"","province_id":"{dpcode}","pagesize":10,"page":1}}&date={self.get_timestamp()}&version=2'
            data_str = self.get_ss(params)
            url = 'https://topm.canyin88.com/api/v2/analyse/brandStoreInfo?data={}'.format(data_str)
            meta['dpcode'] = dpcode
            yield MyRequests(url=url, headers=self.header, callback=self.get_city, level=3, meta=meta)

    def get_city(self, response):
        meta = response.meta
        data = json.loads(response.text).get('data')
        total = data.get('total')
        if total > 0:
            pages = int(total/10)+1
            for page in range(1, pages):
                params = f'{{"brand_id":"{meta.get("id")}","city_id":"","province_id":"{meta.get("dpcode")}","pagesize":10,"page":{page}}}&date={self.get_timestamp()}&version=2'
                data_str = self.get_ss(params)
                url = 'https://topm.canyin88.com/api/v2/analyse/brandStoreInfo?data={}'.format(data_str)
                yield MyRequests(url=url, headers=self.header, callback=self.get_city_shop, level=4, meta=meta)

    def get_city_shop(self, response):
        meta = response.meta
        data_msg = json.loads(response.text).get('data')
        if data_msg:
            data_list = data_msg.get('data')
            for data in data_list:
                meta['province_name'] = data.get('province_name')
                meta['city_name'] = data.get('city_name')
                meta['store_name'] = data.get('store_name')
                meta['star_score'] = data.get('star_score')
                meta['avg_price'] = data.get('avg_price')
                meta['store_id'] = data.get('store_id')
                # self.prints(meta)
                self.r.sadd('hongcan_data_city', meta['store_id'])
                self.kafka_producer('boss.de_nine.spider.hongcanApp', json.dumps(meta, ensure_ascii=False))

    def get_ss(self, ss):
        js = ""
        fp1 = open('./a.js', encoding='utf-8')
        js += fp1.read()
        fp1.close()
        ctx2 = execjs.compile(js)
        return ctx2.call('encryptWithAES', ss)


if __name__ == '__main__':
    start_run = HongcanCitySpider()
    start_run.run()