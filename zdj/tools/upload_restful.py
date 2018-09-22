# encoding: utf-8
from flask_restful import Api,Resource, reqparse
from flask import Flask
from werkzeug import datastructures
import uuid
import os

app = Flask(__name__)
api = Api(app)


class UploadFileAPI(Resource):
    def post(self):
        parse = reqparse.RequestParser()
        # 此处应对应input里的name，通过append将upload的文件合并到一个参数内，遍历得到的文件
        # name="input-b6[]"
        parse.add_argument('input-b6[]', type=datastructures.FileStorage, location='files', action='append')
        args = parse.parse_args()
        file_streams = args['input-b6[]']  # 获取上传的文件列表
        for file_stream in file_streams:
            # 遍历上传列表中的单个文件
            file_sn = file_stream.filename
            # 生成随机的文件名
            uuid_str = uuid.uuid4().hex
            new_filename = '{0}{1}'.format(uuid_str, os.path.splitext(file_sn)[1])
            file_stream.save(new_filename)


api.add_resource(UploadFileAPI, '/upload')


if __name__ == '__main__':
    app.run(debug=True,port=8081)