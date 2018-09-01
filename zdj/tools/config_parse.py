#!encoding:utf-8
import configparser

config = configparser.ConfigParser()
config['UserInfo'] = {'username': 'huangzirong184', 'password': ''}
config['modules'] = {'interval(minutes)': 5, 'alert': 'True',
                     'down_script': 'True', 'script_path': r'D:\script',
                     'type':'collect;modify'}
with open('config.cnf', 'w') as conf_file:
    config.write(conf_file)