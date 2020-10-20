# -*- coding: utf-8 -*-
"""
@file   : db_handle.py
@author : Andy Zhang
@time   : 2020/10/15 14:41
@Desc   : 
"""
import os
import pickle
from conf.settings import DB_PATH


def save_data(obj):
    '''
    保存数据
    :param obj:要保存的对象
    :return:
    '''
    folder = obj.__class__.__name__  # 获取对象的类名当做文件夹名
    role_path = os.path.join(DB_PATH, folder)  # eg:CourseSystem/db/Admin/
    if not os.path.exists(role_path):
        os.mkdir(role_path)
    user_path = os.path.join(role_path, obj.name)  # 用户名当做文件名
    with open(user_path, 'wb') as f:
        pickle.dump(obj, f)


def select_data(cls, username):
    '''
    查询用户信息
    :param cls:当前用户的类，用户获取类名（保存用户信息的文件夹名称）
    :param username: 要查询的用户名
    :return: 返回用户对象或None
    '''
    folder = cls.__name__  # 获取类名当做文件夹名
    role_path = os.path.join(DB_PATH, folder)
    user_path = os.path.join(role_path, username)  # 用户名当做文件名
    if os.path.exists(user_path):  # 判断用户是否存在
        with open(user_path, 'rb') as f:
            obj = pickle.load(f)
            return obj
