#!/bin/bash

# 进入 Python 虚拟环境
#source activate
#conda activate qingchuan

# 查询并杀死进程
#if ps aux | grep -q 'search_engine_server.py'; then
#    # 如果进程存在，则杀死它
#    echo "正在杀死进程..."
#    pkill -f search_engine_server.py
#    sleep 1
#fi

# 启动 Python 文件
echo "正在启动进程..."
source /home/work/py3.7/bin/activate && cd /home/work/single/spider/lqc_spiders/qimaidata/ && nohup python -u qimaidata.py>> /dev/null 2>&1 &