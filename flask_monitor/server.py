# encoding: utf-8
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_monitor.models.BaseModels import LinuxServerModel, ServerStatusModel
from flask_monitor.database import DB_session
from sqlalchemy import and_
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_monitor.logger import logger
from utils import table_obj_2_dict
from conf import errors

app = Flask(__name__)
api = Api(app, catch_all_404s=True, errors=errors)


class LinuxServer(Resource):
    def get(self):
        """
        获取主机的信息
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('server_id', type=int)
        args = parser.parse_args()
        server_id = args['server_id']
        session = DB_session()
        match_servers = session.query(LinuxServerModel).filter(LinuxServerModel.id==server_id).all()
        if len(match_servers) == 1:
            match_server = match_servers[0]
            logger.debug('get LinuxServer: {0}'.format(match_server))
            # 获取服务器的当前状态,以采集时间倒序
            server_status = session.query(ServerStatusModel).filter(
                ServerStatusModel.server_id==match_server.id).order_by(ServerStatusModel.collect_time.desc()).first()
            match_server_dict = table_obj_2_dict(match_server)  # 对结果对象转为dict
            if server_status:
                server_status_dict = table_obj_2_dict(server_status)  # 对结果对象转为dict
                # 服务器status为从属状态
                match_server_dict['status'] = server_status_dict
            session.close()
            return {'server': match_server_dict}, 200
        else:
            #  没有匹配的LinuxServer结果或结果不为1
            logger.debug('match LinuxServer count is {0}.'.format(len(match_servers)))
            session.close()
            return {'server': None}, 404

    def post(self):
        """
        客户端post请求，将收集的客户端服务器信息反馈到服务端
        :param: hostname：主机ming
        :param: cpu_percent: 主机CPU利用率
        :param: mem_usage: 内存利用率
        :param: collect_time: 采集时间
        :return: ip_addr: 服务器IP地址
        """
        parser = reqparse.RequestParser()
        # 控制输入参数必须包含hostname和ip_addr
        parser.add_argument('hostname',type=str, required=True, help='hostname is required')
        parser.add_argument('ip_addr', type=str, required=True, help='ip address is required')
        parser.add_argument('cpu_percent', type=float)
        parser.add_argument('mem_percent', type=float)
        parser.add_argument('collect_time', type=str)
        parser.add_argument('cpu_core_num', type=int)
        parser.add_argument('memory', type=float)

        args = parser.parse_args()
        in_hostname = args['hostname']
        in_ip_addr = args['ip_addr']
        in_mem_percent = args['mem_percent']
        in_cpu_percent = args['cpu_percent']
        in_cpu_core_num = args['cpu_core_num']
        in_memory = args['memory']

        # 对采集时间进行格式化
        in_collect_time= datetime.strptime((args['collect_time'] if args['collect_time'] is not None else '1900/01/01 00:00:00'), '%Y/%m/%d %H:%M:%S')
        session = DB_session()
        match_servers = session.query(LinuxServerModel).filter(and_(LinuxServerModel.hostname == in_hostname,
                                                                    LinuxServerModel.ip_addr == in_ip_addr)).all()
        if len(match_servers) == 0:
            logger.debug('init new server and add collect data')
            new_linux_server = LinuxServerModel(hostname=in_hostname, ip_addr=in_ip_addr, cpu_core_num=in_cpu_core_num,
                                                memory=in_memory)
            session.add(new_linux_server)
            session.flush()
            session.commit()
            return {'id': new_linux_server.id, 'hostname': new_linux_server.hostname}, 200
        elif len(match_servers) == 1:
            logger.debug('add collect data')
            if args['collect_time'] is None:
                # 没有采集数据时新增服务器问题
                logger.warning('collect_time is None,not add collect data')
                return {'collect_id': None}, 406
            match_server = match_servers[0]  # 获取匹配的服务器记录
            logger.debug('match server {0}'.format(match_server))
            new_collect = ServerStatusModel(server_id=match_server.id, cpu_percent=in_cpu_percent,
                                            mem_percent=in_mem_percent,collect_time=in_collect_time)
            try:
                session.add(new_collect)
                session.flush()
                session.commit()
                logger.debug('add collect data success! item {0}'.format(new_collect))
            except SQLAlchemyError as e:
                logger.error(e)
                logger.error("unable to insert collect data to database.")
                return {'collect_id': None}, 406
            return {'server_id': match_server.id, 'collect_id': new_collect.id}, 200
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

