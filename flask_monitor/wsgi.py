# encoding: utf-8
import hmac
import hashlib
import json
from flask import Flask, make_response
from flask_restful import Api, Resource, reqparse, marshal_with, fields, abort
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from flask_monitor.logger import logger
from flask_monitor.utils import table_obj_2_dict
from flask_monitor.conf import errors
from flask_httpauth import HTTPTokenAuth

from itsdangerous import JSONWebSignatureSerializer as UnExpiredSerializer
from itsdangerous import SignatureExpired, BadSignature
from flask_monitor.database import db
from flask_monitor.models.BaseModels import LinuxServerModel, ServerStatusModel, UserModel
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SECRET_KEY'] = b'this is secure'
# 使用mysql驱动连接mysql库
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:hujnhu123@192.168.113.1/test'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
# 通过自定义的errors指定出错时的返回信息，改掉默认的500错误的提醒，可以自定义提醒内容
api = Api(app, catch_all_404s=True, errors=errors)

db.init_app(app)
# TODO: 通过flask migrate 控制数据库初始化/升级
migrate = Migrate(app, db)

auth = HTTPTokenAuth()
# 使用会超时的token
# from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
# s_obj = Serializer(app.config['SECRET_KEY'], expires_in=6000)
# 使用不会超时的token
s_obj = UnExpiredSerializer(app.config['SECRET_KEY'])


def generate_auth_token(user_id):
    return s_obj.dumps({'user_id': user_id})


@auth.verify_token
def verify_token(token):
    in_user_id = None
    if token is None or len(token) == 0:
        return False
    try:
        in_user_id = s_obj.loads(token)['user_id']
    except SignatureExpired:
        # 如果token过期，将认证失败
        return False
    except BadSignature:
        return False
    else:
        # 如果token未过期，则进行用户的认证
        match_user = UserModel.query.filter_by(id=in_user_id).first()
        if match_user:
            logger.info("user {0} match success!".format(match_user.id))
            return True
        else:
            return False


class User(Resource):
    user_field = {
        'user': fields.Nested({
            'username': fields.String,
            'email': fields.String
        })
    }

    @marshal_with(fields=user_field, envelope='user')
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('username', type=str, required=True, help='username is required.')
        args = parser.parse_args()
        match_user = UserModel.query.filter_by(username=args['username']).all()
        if len(match_user) == 0:
            abort(404, message='username {0} not found!'.format(args['username']))
        elif len(match_user) == 1:
            return {'user': match_user}
        else:
            abort('500', message='username {0} duplicate!'.format(args['username']))

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
            if match_user.password != password_hash:
                abort(401, message='password error')
            token = generate_auth_token(match_user.id)
            res = make_response(json.dumps({'token': token.decode('ascii'), 'id': match_user.id}))
            return res
        elif len(match_users) == 0:
            new_user = UserModel(username=args['username'], password=password_hash, email=args['email'])
            db.session.add(new_user)
            db.session.commit()
            token = generate_auth_token(new_user.id)
            # TODO: 此处应该返回201，表示资源已创建
            res = make_response(json.dumps({'token': token.decode('ascii'), 'id': new_user.id}))
            return res
        else:
            abort(404, message='query user {0} error.'.format(args['username']))
            # return {'message': 'query user error'}, 404


class LinuxServer(Resource):
    # 使用http-auth进行登录认证
    decorators = [auth.login_required]
    linux_field = {
        'collect_time': fields.DateTime,
        'server': fields.Nested({
            'id': fields.Integer,
            'ip_address': fields.String,
            'cpu_core_num': fields.Integer,
            'memory': fields.Float
        }),
        'server_status': fields.Nested({
            'server_id': fields.Integer,
            'cpu_percent': fields.Float,
            'mem_percent': fields.Float,

        })
    }

    @marshal_with(linux_field, envelope='linux_server')
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
            return {'collect_time': server_status.collect_time,
                    'server': match_server,
                    'server_status': server_status}
        else:
            #  没有匹配的LinuxServer结果或结果不为1
            logger.debug('match LinuxServer count is {0}.'.format(len(match_servers)))
            # session.close()
            # 通过flask_restful的abort函数进行返回
            abort(404, message='linux server {0} not found.'.format(server_id))

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
            # TODO: 此处应该返回201，表示资源已创建
            return {'id': new_linux_server.id, 'hostname': new_linux_server.hostname}, 201
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
    app.run(port=8080)

