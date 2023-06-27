# -*- coding: utf-8 -*-

# 并发数
PREFETCH_COUNT = 50

# 最大优先级数
X_MAX_PRIORITY = 15

# 是否开启断点
Breakpoint = True

# 超时时间设置
TIME_OUT = 40

# 最大重试次数
max_request = 4
retry_http_codes = [209, 301, 302, 400, 403, 404, 405, 408, 412, 429, 500, 502, 503, 504, 505, 521]  # 允许重试的状态码

UA_PROXY = True  # 是否开启UA池代理
IS_PROXY = True  # 是否开启代理
IS_SAMEIP = False  # 是否开启同一ip会话
Agent_whitelist = ['127.0.0.1']  # 代理白名单

# 连接redis数据库
REDIS_HOST_LISTS = [{'yours': '6379'}]  # 主机名
# REDIS_PARAMS = {'password': 'password'} # 单机情况下,密码没有的不设置
redis_connection = False  # 是否开启redis连接

# 连接kafka数据库
kafka_servers = {
    # 'server': '10.64.2.190:2181',  # 外网
    'server': ['10.64.2.190:9092', '10.64.2.47:9092', '10.64.2.104:9092', '10.64.2.121:9092', '10.64.2.24:9092',
               '10.64.2.133:9092', '10.64.2.161:9092', '10.64.2.109:9092', '10.64.2.29:9092', '10.64.2.222:9092'],  # 外网
    'security_protocol': "SASL_PLAINTEXT", 'sasl_mechanism': "SCRAM-SHA-256",
    'sasl_plain_username': "de_nine",
    'sasl_plain_password': "8iDzhVExautncdBd6puPtxJudQe5KH5L",
}
kafka_connection = True  # 是否开启kafka连接

# 连接mysql
Mysql = {
    # 线下
    'MYSQL_HOST': '192.168.22.81',
    # 线上
    # 'MYSQL_HOST': '127.0.0.1',
    'MYSQL_DBNAME': 'spider',
    'MYSQL_USER': 'spider',
    'MYSQL_PASSWORD': 'b@4RkJFo!6yL',
    'PORT': 13307
}

OTHER_Mysql = {
    'MYSQL_HOST': 'yours',
    'MYSQL_DBNAME': 'yours',
    'MYSQL_USER': 'yours',
    'MYSQL_PASSWORD': 'yours',
    'PORT': 3306,
}
IS_INSERT = True  # 是否开启mysql连接
OTHER_DB = False  # 是否开启第二个数据库连接

# RabbitMQ服务器的地址及各项参数
Rabbitmq = {
    'Sgin': 'lqc',
    'username': 'admin',
    'password': 'admin',
    # 'host': '192.168.22.81',  # 线下
    'host': '127.0.0.1',  # 线上
    'port': 5672,
    'max_retries': 3,  # 最大重连次数
    'async_thread_pool_size': 4,  # 异步发送线程池
}
message_ttl = 86400000
Auto_clear = True  # 重启是否自动清空队列
Asynch = True  # 是否开启异步生产
IS_connection = True  # 是否开启Rabbitmq连接
Waiting_time = 300  # 允许队列最大空置时间(秒),切记要比请求超时时间长
Delay_time = 4  # 自动关闭程序最大延迟时间

# custom_settings = {}

# log_path = '/Users/admin/Downloads/single_process-main/log_filed'  # 日志保存路径
log_path = '/home/work/single/log_filed'  # 日志保存路径
log_level = 'DEBUG'  # 日志级别

# 邮件发送
EMAIL_CONFIG = {
    'email_host': "smtp.163.com",  # 设置服务器
    'email_user': 'yours',  # 用户名
    'email_pass': 'yours',  # 口令
    'email_port': 25,
    'sender': 'yours',  # 发送者
    'receivers': 'yours',  # 接收邮件，可设置为你的QQ邮箱或者其他邮箱，发送多人用逗号隔开
}

access_key_id = 'yours'
access_key_secret = 'yours'
bucket_name = 'yours'
endpoint = 'yours'  # 外网
# endpoint = 'oss-cn-beijing-internal.aliyuncs.com'  # 内网
