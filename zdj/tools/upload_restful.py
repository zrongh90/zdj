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
        parse.add_argument('file_s', type=datastructures.FileStorage, location='files')
        args = parse.parse_args()
        file_stream = args['file_s']
        file_sn = file_stream.filename
        uuid_str = uuid.uuid4().hex
        new_filename = '{0}{1}'.format(uuid_str, os.path.splitext(file_sn)[1])
        file_stream.save(new_filename)


api.add_resource(UploadFileAPI, '/upload')


if __name__ == '__main__':
    app.run(debug=True,port=8081)