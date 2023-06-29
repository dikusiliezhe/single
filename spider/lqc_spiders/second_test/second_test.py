# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spider')[0])
from config.all_config import *


class SecondTestSpider(Manager):
    name = 'second_test'

    def __init__(self):
        Manager.__init__(self)
        # self.online = True
        self.header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        }

    def start_requests(self):
        url = 'https://www.baidu.com/'
        yield MyRequests(url=url, headers=self.header, callback=self.parse, level=1)

    def parse(self, response):
        print(response.text)


if __name__ == '__main__':
    start_run = SecondTestSpider()
    start_run.run()