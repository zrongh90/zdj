# encoding: utf-8
import collections
from datetime import datetime, timedelta
ip_count = collections.defaultdict(int)
with open('tools/access_log') as f:
    for line in f:
        split_line = line.split()
        current_time = datetime.strptime('2018-07-11 14:35:34', '%Y-%m-%d %H:%M:%S')
        inside_one_minute = current_time - timedelta(minutes=1)
        print(datetime.strptime(split_line[3][1:], '%d/%b/%Y:%H:%M:%S'))
        if datetime.strptime(split_line[3][1:], '%d/%b/%Y:%H:%M:%S') > inside_one_minute:
            ip_count[split_line[0]] += 1
    print(ip_count)