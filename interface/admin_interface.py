# -*- coding: utf-8 -*-
"""
@file   : admin_interface.py
@author : Andy Zhang
@time   : 2020/10/15 15:21
@Desc   : 
"""
from db.models import Admin, Campus, Course, Teacher


def admin_register(username, pwd):
    '''
    管理员注册接口
    :param username:注册的用户名
    :param pwd: 注册的密码
    :return: 返回注册结果True  False
    '''
    if Admin.select(username):#判断用户是否已存在
        return False, '用户已存在'
    # 用户不存在则创建用户
    admin_obj = Admin(username, pwd)
    admin_obj.save()  # 保存用户
    return True, f'{username}用户注册成功!'


# def admin_login(username, pwd):
#     '''
#     登录接口
#     :param username:
#     :param pwd:
#     :return:
#     '''
#     if not Admin.select(username):
#         return False, '用户不存在'
#     admin_obj = Admin.select(username)
#     if pwd == admin_obj.pwd:
#         return True, f'{username}用户登录成功!'
#     else:
#         return False, '用户密码错误!'


def admin_create_campus(campus_name, campus_addr, creator):
    '''
    创建学校接口
    :param campus_name: 学校名称
    :param campus_addr: 学校地址
    :param creator: 创建者（管理员名称）
    :return:
    '''
    # 判断学校是否已存在
    if Campus.select(campus_name):
        return False, '学校已存在'
    admin_obj = Admin.select(creator)  # 不存在是，拿到创建学校的用户--管理员
    admin_obj.create_campus(campus_name, campus_addr)  # 用户来创建学校
    return True, f'{campus_name}创建成功！'


def admin_create_course(campus_name, course_name, course_price, creator):
    campus_obj = Campus.select(campus_name)  # 获取到学校对象
    if course_name.lower() in campus_obj.course_list:
        return False, f'【{course_name}】课程已存在！'

    admin_obj = Admin.select(creator)  # 不存在，拿到创建学校的用户--管理员
    admin_obj.create_course(campus_obj, course_name, course_price)
    return True, f'【{course_name}】创建成功'


def admin_create_teacher(creator, teacher_name, teacher_pwd='123'):
    '''
    创建教师接口
    :param creator: 创建教师的管理员用户
    :param teacher_name: 教师姓名
    :param teacher_pwd: 教师密码
    :return: True or False
    '''
    if Teacher.select(teacher_name):  # 先检查教师是否已存在
        return False, '教师已存在'
    admin_obj = Admin.select(creator)
    admin_obj.create_teacher(teacher_name, teacher_pwd)  # 调用管理员方法创建教师
    return True, f'教师{teacher_name}创建成功'
