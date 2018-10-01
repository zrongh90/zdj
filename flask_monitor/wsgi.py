# encoding: utf-8
import hmac
import hashlib
from flask import Flask
from flask_restful import Api, Resource, reqparse

# from flask_monitor.database import DB_session
from sqlalchemy import and_
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_monitor.logger import logger
from flask_monitor.utils import table_obj_2_dict
from flask_monitor.conf import errors
from flask_httpauth import HTTPTokenAuth
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from itsdangerous import SignatureExpired
from flask_monitor.database import db
from flask_monitor.models.BaseModels import LinuxServerModel, ServerStatusModel, UserModel
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = b'this is secure'
# 使用mysql驱动连接mysql库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hujnhu123@192.168.113.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
api = Api(app, catch_all_404s=True, errors=errors)
db.init_app(app)
# TODO: 通过flask migrate 控制数据库初始化/升级
migrate = Migrate(app, db)

auth = HTTPTokenAuth()
s_obj = Serializer(app.config['SECRET_KEY'], expires_in=6000)




def generate_auth_token(user_id):
    return s_obj.dumps({'user_id': user_id})


@auth.verify_token
def verify_token(token):
    in_user_id = None
    try:
        in_user_id = s_obj.loads(token)['user_id']
    except SignatureExpired:
        # 如果密码获取，将认证失败
        return False
    else:
        # 如果token未过期，则进行用户的认证
        # session = DB_session()
        UserModel.query.filter_by(id=in_user_id).first()
        # session.query(UserModel).filter(UserModel.id==in_user_id).get
        print('get token and verify')
        return True


class User(Resource):
    def get(self):

        pass

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help="username is required")
        parser.add_argument('password', type=str, required=True, help="password is required")
        parser.add_argument('email', type=str)
        args = parser.parse_args()
        password_hash = hmac.new(app.secret_key,args['password'].encode('utf-8'), hashlib.sha256).hexdigest()
        match_users = UserModel.query.filter_by(name=args['username']).all()
        if len(match_users) == 1:
            match_user = match_users[0]
            token = generate_auth_token(match_user.id)
            return {'token': token.decode('ascii')}, 200
        elif len(match_users) == 0:
            new_user = UserModel(name=args['username'], password=password_hash, email=args['email'])
            db.session.add(new_user)
            db.session.commit()
            token = generate_auth_token(new_user.id)
            return {'token': token.decode('ascii')}, 200
        else:
            return {'message': 'query user error'}, 404


class LinuxServer(Resource):
    # 使用http-auth进行登录认证
    decorators = [auth.login_required]

    def get(self):
        """
        获取主机的信息
        :return:
        """
        parser = reqparse.RequestParser()
        parser.add_argument('server_id', type=int)
        args = parser.parse_args()
        server_id = args['server_id']
        match_servers = LinuxServerModel.query.filter_by(id=server_id).all()
        # match_servers = session.query(LinuxServerModel).filter(LinuxServerModel.id==server_id).all()
        if len(match_servers) == 1:
            match_server = match_servers[0]
            logger.debug('get LinuxServer: {0}'.format(match_server))
            # 获取服务器的当前状态,以采集时间倒序
            server_status = ServerStatusModel.query.filter_by(server_id=match_server.id).\
                order_by(ServerStatusModel.collect_time.desc()).first()
            # server_status = session.query(ServerStatusModel).filter(
            #     ServerStatusModel.server_id == match_server.id).order_by(ServerStatusModel.collect_time.desc()).first()
            match_server_dict = table_obj_2_dict(match_server)  # 对结果对象转为dict
            if server_status:
                server_status_dict = table_obj_2_dict(server_status)  # 对结果对象转为dict
                # 服务器status为从属状态
                match_server_dict['status'] = server_status_dict
            # session.close()
            return {'server': match_server_dict}, 200
        else:
            #  没有匹配的LinuxServer结果或结果不为1
            logger.debug('match LinuxServer count is {0}.'.format(len(match_servers)))
            # session.close()
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
        # session = DB_session()
        match_servers = LinuxServerModel.query.filter_by(hostname=in_hostname).filter_by(ip_address=in_ip_addr).all()
        # match_servers = session.query(LinuxServerModel).filter(and_(LinuxServerModel.hostname == in_hostname,
        #                                                             LinuxServerModel.ip_addr == in_ip_addr)).all()
        if len(match_servers) == 0:
            logger.debug('init new server and add collect data')
            new_linux_server = LinuxServerModel(hostname=in_hostname, ip_address=in_ip_addr, cpu_core_num=in_cpu_core_num,
                                                memory=in_memory)
            db.session.add(new_linux_server)
            db.session.commit()
            # session.add(new_linux_server)
            # session.flush()
            # session.commit()
            return {'id': new_linux_server.id, 'hostname': new_linux_server.hostname}, 200
        elif len(match_servers) == 1:
            logger.debug('add collect data')
            if args['collect_time'] is None:
                # 没有采集数据时新增服务器问题
                logger.warning('collect_time is None,not add collect data')
                return {'collect_id': None}, 406
            match_server = match_servers[0]  # 获取匹配的服务器记录
            logger.debug('match server {0}'.format(match_server))
            if match_server.cpu_core_num != in_cpu_core_num or match_server.memory != in_memory:
                # 考虑主机的可变参数的变化，例如CPU数目/内存大小
                logger.debug('update server changeable parameter')
                match_server.cpu_core_num = in_cpu_core_num
                match_server.memory = in_memory
            new_collect = ServerStatusModel(server_id=match_server.id, cpu_percent=in_cpu_percent,
                                            mem_percent=in_mem_percent,collect_time=in_collect_time)
            try:
                db.session.add(new_collect)
                db.session.commit()
                # session.add(new_collect)
                # session.flush()
                # session.commit()
                logger.debug('add collect data success! item {0}'.format(new_collect))
            except SQLAlchemyError as e:
                logger.error(e)
                logger.error("unable to insert collect data to database.")
                return {'collect_id': None}, 406
            return {'server_id': match_server.id, 'collect_id': new_collect.id}, 200
        else:
            print('match server error')
        # session.close()
        # TODO: 将获取的结果写入到数据库，考虑时序性数据问题
        return None
        # return {'server_id': new_id, 'hostname': hostname, 'cpu_percent': cpu_percent}


class WasServer(Resource):
    def get(self):
        pass

    def post(self):
        pass


api.add_resource(LinuxServer, '/LinuxServer')
api.add_resource(User, '/User')


if __name__ == '__main__':
    app.run(debug=True, port=8080)

