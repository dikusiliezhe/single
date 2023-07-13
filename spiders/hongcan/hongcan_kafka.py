# -*- coding: utf-8 -*-
import json
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *


class HongcanKafkaSpider(Manager):
    name = 'hongcan_kafka'
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
                print(value)
                self.kafka_producer('boss.de_nine.spider.hongcanApp_brand', json.loads(value))

            # 如果cursor值为0，表示迭代完成，退出循环
            if cursor == 0:
                break
        url = 'https://www.baidu.com/'
        yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    start_run = HongcanKafkaSpider()
    start_run.run()