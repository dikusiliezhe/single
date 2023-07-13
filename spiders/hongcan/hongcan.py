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


class HongcanSpider(Manager):
    name = 'hongcan'
    custom_settings = {
        'PREFETCH_COUNT': 5,
    }

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36 MicroMessenger/6.8.0(0x16080000) NetType/WIFI MiniProgramEnv/Mac MacWechat/WMPF XWEB/30515',
            'Content-Type': 'application/json'
        }

    def start_requests(self):
        pages = 1607
        for page in range(1, pages):
        # for page in range(1, 2):
            data = f'{{"master_type":"0","second_type":"","city_id":"","province_id":"","order_by":"store_count","desc":"desc","pagesize":10,"page":{page},"keyword":"","top_bg":""}}&date={self.get_timestamp()}&version=2'
            data_str = get_ss(data)
            url = 'https://topm.canyin88.com/api/v2/brands/search?data={}'.format(data_str)
            yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        data_list = json.loads(response.text).get('data').get('data')
        for data in data_list:
            id = data.get('id')
            id_exist = self.r.hexists('hongcan_data', id)
            if not id_exist:
                params = f'{{"brand_id":"{id}","uid":"oge6wv9dzlvAT4UEj-x527YjrlZU","token":"taxRhjuKvyIaVkI40B8Ccw==","from":"5"}}&date={self.get_timestamp()}&version=2'
                data_str = get_ss(params)
                url = 'https://topm.canyin88.com/api/v2/brands/detail?data={}'.format(data_str)
                yield MyRequests(url=url, headers=self.header, callback=self.get_detail, level=2)



    def get_detail(self, response):
        data = json.loads(response.text).get('data')
        try:
            brand_id = data.get('brand_id')
            name = data.get('name')
            establish = data.get('establish')
            store_count = data.get('brands_version_data').get('store_count') if data.get('brands_version_data') else ''
            avg_price = data.get('brands_version_data').get('avg_price') if data.get('brands_version_data') else ''
            score = data.get('brands_version_data').get('score') if data.get('brands_version_data') else ''
            typeMaster = data.get('typeMaster')
            company_desc = data.get('company_desc')
            company_name = data.get('company_name')
            company_addr = data.get('company_addr')
            company_time = data.get('company_time')
            company_url = data.get('company_url')
            company_contact_phone = data.get('company_contact_phone')
            company_license_number = data.get('company_license_number')
            company_scope = data.get('company_scope')
            province_store = data.get('province_store')
            msg_dic = {'brand_id':brand_id, 'name':name, 'establish':establish,  'store_count':store_count,  'avg_price':avg_price,'score': score, 'typeMaster':typeMaster,  'company_desc':company_desc,  'company_name':company_name,  'company_addr':company_addr,  'company_time':company_time,  'company_url':company_url,  'company_contact_phone':company_contact_phone,  'company_license_number':company_license_number,  'province_store':province_store, 'company_scope':company_scope}
            self.set_redis_value(redis_name='hongcan_data', key=brand_id, value=json.dumps(msg_dic, ensure_ascii=False))
            self.prints(msg_dic)
        except:
            self.logger.warn(response.url)


if __name__ == '__main__':
    start_run = HongcanSpider()
    start_run.run()
