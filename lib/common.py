# -*- coding: utf-8 -*-
"""
@file   : common.py
@author : Andy Zhang
@time   : 2020/10/15 14:40
@Desc   : 
"""
# from core import admin, student, teacher


# 多用户登录认证装饰器
def auth(role):
    '''
    :param role: 登录的角色：学生、教师、管理员
    :return:
    '''
    from core import admin, student, teacher
    def login_auth(func):
        def inner(*args, **kwargs):
            if role == 'admin':
                if admin.user_state['user']:  # 不为None说明已登录
                    res = func(*args, **kwargs)
                    return res
                else:
                    admin.login()  # 让用户去登录
            elif role == 'teacher':
                if teacher.user_state['user']:  # 不为None说明已登录
                    res = func(*args, **kwargs)
                    return res
                else:
                    teacher.login()  # 让用户去登录
            elif role == 'student':
                if student.user_state['user']:  # 不为None说明已登录
                    res = func(*args, **kwargs)
                    return res
                else:
                    student.login()  # 让用户去登录
            else:
                print('该视图没有权限')

        return inner

    return login_auth
