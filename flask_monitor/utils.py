# encoding: utf-8
def table_obj_2_dict(in_obj):
    dict_obj = {}
    for column in in_obj.__table__.columns:
        dict_obj[column.name] = str(getattr(in_obj, column.name))
    return dict_obj
