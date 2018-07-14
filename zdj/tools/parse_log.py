# encoding: utf-8
import sys
from datetime import datetime, timedelta
count_minutes = int(sys.argv[1])
with open('/var/log/httpd/access_log') as f:
    # current_time = datetime.now()
    count = 0
    current_time = datetime.strptime('2018-07-11 14:35:34', '%Y-%m-%d %H:%M:%S')
    for line in f:
        split_line = line.split()
        inside_one_minute = current_time - timedelta(minutes=count_minutes)
        # print(datetime.strptime(split_line[3][1:], '%d/%b/%Y:%H:%M:%S'))
        if datetime.strptime(split_line[3][1:], '%d/%b/%Y:%H:%M:%S') > inside_one_minute:
            count += 1
            # ip_count[split_line[0]] += 1
    print(count)