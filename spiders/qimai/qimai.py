# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)).split('spiders')[0])
from config.all_config import *
import execjs

class QimaiSpider(Manager):
    name = 'qimai'

    custom_settings = {
        'PREFETCH_COUNT': 10,
        # 'retry_http_codes': [202, 412],
        'Waiting_time': 300,
        'IS_PROXY': True,
        'IS_SAMEIP': False,
        'UA_PROXY': False,
        # 'X_MAX_PRIORITY': 15,
        # 'max_request': 1,
        # 'PREFETCH_COUNT': 50
    }


    def __init__(self):
        Manager.__init__(self)
        self.header = {
            'authority': 'api.qimai.cn',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            # 'cookie': 'PHPSESSID=ukhsgj4qacovi7dqh8bolanmvp; tgw_l7_route=1ed618a657fde25bb053596f222bc44a',
            'origin': 'https://www.qimai.cn',
            'referer': 'https://www.qimai.cn/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36'
        }
        self.header2 = {
            'authority': 'api.qimai.cn',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'zh-CN,zh;q=0.9',
            'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'origin': 'https://www.qimai.cn',
            'referer': 'https://www.qimai.cn/',
            'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            # 'Cookie': 'PHPSESSID=hgaqppun755a6jgt0o7ihivuul; tgw_l7_route=29ef178f2e0a875a4327cbfe5fbcff7e'
        }
        self.app_list = [{'name': 'boss直聘', 'appid': '887314963', 'pages': 336}]
        # self.online=True

    def start_requests(self):
        for app in self.app_list:
            parms_dict = {
                'sdate': datetime.date.today().strftime("%Y-%m-%d"),
                'edate': (datetime.date.today() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
                'appid': app['appid'],
                'version': 'ios14',
                'device': 'iphone'}
            url_list = [
                {'url': 'https://api.qimai.cn/appDetail/keywordDetail?analysis={}'.format(
                    self.get_ss(
                        {'url': "/appDetail/keywordDetail", 'baseURL': "https://api.qimai.cn", 'params': {}, })),
                    'page': app['pages'],
                    'data': 'country=cn&sdate={}&edate={}&appid={}&version={}&device={}&hints_min=&hints_max=&ranking_min=&ranking_max=&result_min=&result_max=&search=&quick_rank=all&type=all&page={}&size=100&sort=srank&sort_type=asc&current_type=all',
                },

            ]
            for url_page in url_list:
                if self.pages:
                    pages = self.pages
                else:
                    pages = url_page.get('page')
                for page in range(1, pages):
                    url = url_page.get('url')
                    # url = 'https://api.qimai.cn/appDetail/keywordDetail?analysis=dkZJBhgIPR9BUF4PSwpcTxIJFQw8HA5UWFsjR1MPA1dWU1pMQUoAcRRQ'
                    data = url_page.get('data')
                    data = data.format(parms_dict["sdate"], parms_dict["edate"], parms_dict["appid"],
                                       parms_dict["version"], parms_dict["device"], page)
                    yield MyFormRequests(url=url, headers=self.header2, callback=self.parse, level=1, data=data,
                                         meta={'parms': parms_dict, 'app': app})

    def parse(self, response):
        parms = response.meta.get('parms')
        app = response.meta.get('app')
        now_time = datetime.datetime.now().replace(minute=0, second=0, microsecond=0).strftime("%Y-%m-%d %H:%M:%S")
        stamp = self.time2stamp(now_time, level=1000)
        data_list = json.loads(response.text).get('data')
        for data in data_list:
            msg_dict = {'app_name': app['name'], 'appid': app['appid'], 'word_name': data['word_name'],
                        'word_id': data['word_id'], 'srank': data['srank'], 'now_time': now_time,
                        'now_time_stamp': stamp}
            self.kafka_producer('boss.de_nine.spider.qimai_App_spider', msg_dict)

    def get_ss(self, ss):
        """
        :param js_path: js文件路径
        :param function_name: 要执行的js方法名
        :param kwargs: 执行js时需要传的参数
        :return: js返回的结果
        """
        js = ""
        fp1 = open('./tools.js', encoding='utf-8')
        js += fp1.read()
        fp1.close()
        ctx2 = execjs.compile(js)
        self.logger.info('55555555555555555')
        return ctx2.call('beforeRequest', ss)


if __name__ == '__main__':
    start_run = QimaiSpider()
    start_run.run()