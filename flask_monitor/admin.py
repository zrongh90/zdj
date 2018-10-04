# encoding: utf-8
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
admin = Admin(name='flask_monitor', template_mode='bootstrap3')
from flask_monitor.database import db
from flask_monitor.models.BaseModels import UserModel, LinuxServerModel, ServerStatusModel, WASServerModel


class UserModelView(ModelView):
    # 排除选定列
    column_exclude_list = ['email']
    # 选中可过滤列
    column_filters = ['username']


# 通过自定义的ModelView去控制admin的功能
admin.add_view(UserModelView(UserModel, db.session))
# 基础的ModelView的绑定方法
admin.add_view(ModelView(LinuxServerModel, db.session))
admin.add_view(ModelView(ServerStatusModel, db.session))
admin.add_view(ModelView(WASServerModel, db.session))