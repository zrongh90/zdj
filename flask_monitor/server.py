# encoding: utf-8
from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_monitor.models.BaseModels import LinuxServerModel
from flask_monitor.database import DB_session
from sqlalchemy import and_
from datetime import datetime

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
        parser.add_argument('memort_percent', type=float)
        parser.add_argument('collect_time', type=str)
        parser.add_argument('ip_addr', type=str)
        args = parser.parse_args()
        in_hostname = args['hostname']
        in_ip_addr = args['ip_addr']
        in_collect_time = args['collect_time']
        in_cpu_percent = args['cpu_percent']
        session = DB_session()
        match_server = session.query(LinuxServerModel).filter(and_(LinuxServerModel.hostname == in_hostname,
                                                                   LinuxServerModel.ip_addr == in_ip_addr)).all()
        if len(match_server) == 0:
            print('init new server and add collect data')
            new_linux_server = LinuxServerModel(hostname=in_hostname, ip_addr=in_ip_addr)
            session.add(new_linux_server)
            session.flush()
            session.commit()
            return {'id': new_linux_server.id, 'hostname': new_linux_server.hostname}
        elif len(match_server) == 1:
            print('add collect data')
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

