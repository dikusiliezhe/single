import logging
# from task_logger import SpiderLog

from kafka import KafkaConsumer

kafka_server = ['10.64.2.190:9092', '10.64.2.47:9092', '10.64.2.104:9092', '10.64.2.121:9092', '10.64.2.24:9092',
                '10.64.2.133:9092', '10.64.2.161:9092', '10.64.2.109:9092', '10.64.2.29:9092',
                '10.64.2.222:9092']

# log = SpiderLog()
# 创建Kafka消费者实例
consumer = KafkaConsumer(
    'boss.de_nine.spider.qimai_App_spider',# 替换成你要消费的Topic名称
    group_id='test11232',
    security_protocol="SASL_PLAINTEXT", sasl_mechanism="SCRAM-SHA-256", sasl_plain_username="de_nine",
    sasl_plain_password="8iDzhVExautncdBd6puPtxJudQe5KH5L",
    api_version=(0, 10, 2),
    bootstrap_servers=kafka_server,  # 替换成消费者组的ID
    # auto_offset_reset='earliest',
)

# 循环消费消息
for message in consumer:
    # 解析消息内容
    topic = message.topic
    partition = message.partition
    offset = message.offset
    value = message.value.decode('utf-8')  # 如果消息是文本形式，需要解码

    # 处理消息
    print(f'Received message: Topic={topic}, Partition={partition}, Offset={offset}, Value={value}')

# 关闭消费者
# consumer.close()
