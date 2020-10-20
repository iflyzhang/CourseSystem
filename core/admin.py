# -*- coding: utf-8 -*-
"""
@file   : admin.py
@author : Andy Zhang
@time   : 2020/10/15 15:22
@Desc   : 
"""
from interface import admin_interface
from interface import common_interface
from lib import common


# 保存用户登录状态
user_state = {
    'user': None
}


def register():
    '''
    管理员注册功能
    :return:
    '''
    while True:
        username = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        re_pwd = input('请确认密码：').strip()
        if pwd != re_pwd:
            print('两次输入密码不一致')
            continue
        flag, msg = admin_interface.admin_register(username, pwd)
        if flag:
            print(msg)
            break  # 注册成功则退出循环
        else:
            print(msg)


def login():
    while True:
        username = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        # flag, msg = admin_interface.admin_login(username, pwd)
        flag, msg = common_interface.login(username, pwd, user_type='admin')
        if flag:
            user_state['user'] = username  # 记录当前用户状态
            print(msg)
            break
        else:
            print(msg)

@common.auth('admin')
def create_campus():
    while True:
        campus_name = input('请输入学校名称：').strip()
        campus_addr = input('请输入学校地址：').strip()
        flag, msg = admin_interface.admin_create_campus(campus_name, campus_addr, user_state.get('user'))
        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('admin')
def create_course():
    while True:
        # 查询所有学校并让用户选择
        flag, values = common_interface.get_all_campus()
        if not flag:  # 没有学校
            print(values)
            break
        # enumerate()用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，
        # 同时列出数据和数据下标
        for index, campus_name in enumerate(values):
            print(f'编号:{index}  课程：{campus_name}')
        choice = input('请输入学校编号：').strip()
        if not choice.isdigit():
            print('请输入数字编号！')
            continue
        if int(choice) not in range(len(values)):
            print('请输入正确的编号！')
            continue
        # 获取选择的学校名称
        campus_name = values[int(choice)]
        course_name = input('请输入课程名称：').strip()
        course_price = input('请输入课程价格：').strip()
        flag, msg = admin_interface.admin_create_course(campus_name, course_name,
                                                        course_price, user_state.get('user'))
        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('admin')
def create_teacher():
    while True:
        teacher_name = input('请输入教师姓名：').strip()
        flag, msg = admin_interface.admin_create_teacher(user_state.get('user'), teacher_name)
        if flag:
            print(msg)
            break
        else:
            print(msg)


func_dict = {
    '1': register,
    '2': login,
    '3': create_campus,
    '4': create_course,
    '5': create_teacher
}


def admin_view():
    while True:
        print('''输入b返回上一层
            ★ 1.注册
            ★ 2.登录
            ★ 3.创建学校
            ★ 4.创建课程
            ★ 5.创建讲师 
        ''')
        choice = input('请输入服务编号：').strip()
        if choice == 'b':
            break
        if choice not in func_dict:
            print('输入有误，请重新输入')
            continue
        func_dict[choice]()
