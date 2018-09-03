# encoding: utf-8
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_monitor.models.BaseModels import LinuxServerModel, ServerStatusModel
from flask_monitor.database import DB_session
from sqlalchemy import and_
from datetime import datetime
from flask_monitor.logger import logger

app = Flask(__name__)
api = Api(app)


class LinuxServer(Resource):
    def get(self):
        """
        获取主机的最新信息
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('server_id', type=int)
        args = parser.parse_args()
        server_id = args['server_id']
        return {'server_id': server_id}

    def post(self):
        """
        客户端post请求，将收集的客户端服务器信息反馈到服务端
        :param: host_name：主机ming
        :param: cpu_percent: 主机CPU利用率
        :param: mem_usage: 内存利用率
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('hostname',type=str)
        parser.add_argument('cpu_percent', type=float)
        parser.add_argument('mem_percent', type=float)
        parser.add_argument('collect_time', type=str)
        parser.add_argument('ip_addr', type=str)
        args = parser.parse_args()
        in_hostname = args['hostname']
        in_ip_addr = args['ip_addr']
        in_mem_percent = args['mem_percent']
        in_cpu_percent = args['cpu_percent']

        # 对采集时间进行格式化
        in_collect_time= datetime.strptime(args['collect_time'], '%Y/%m/%d %H:%M:%S')
        session = DB_session()
        match_servers = session.query(LinuxServerModel).filter(and_(LinuxServerModel.hostname == in_hostname,
                                                                   LinuxServerModel.ip_addr == in_ip_addr)).all()
        if len(match_servers) == 0:

            logger.debug('init new server and add collect data')
            new_linux_server = LinuxServerModel(hostname=in_hostname, ip_addr=in_ip_addr)
            session.add(new_linux_server)
            session.flush()
            session.commit()
            return {'id': new_linux_server.id, 'hostname': new_linux_server.hostname}
        elif len(match_servers) == 1:
            logger.debug('add collect data')
            match_server = match_servers[0]  # 获取匹配的服务器记录
            logger.debug('mathc server {0}'.format(match_server))
            new_collect = ServerStatusModel(server_id=match_server.id, cpu_percent=in_cpu_percent,
                                            mem_percent=in_mem_percent,collect_time=in_collect_time)
            session.add(new_collect)
            session.flush()
            session.commit()
            logger.debug('add collect data success! item {0}'.format(new_collect))
            return {'server_id': match_server.id, 'collect_id': new_collect.id}
        else:
            print('match server error')
        session.close()
        # TODO: 将获取的结果写入到数据库，考虑时序性数据问题
        return None
        # return {'server_id': new_id, 'hostname': hostname, 'cpu_percent': cpu_percent}


class WasServer(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(LinuxServer, '/LinuxServer')


if __name__ == '__main__':
    app.run(debug=True, port=8080)

