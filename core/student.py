# -*- coding: utf-8 -*-
"""
@file   : student.py
@author : Andy Zhang
@time   : 2020/10/15 15:22
@Desc   : 
"""
from interface import student_interface
from interface import common_interface
from lib import common

# 保存用户登录状态
user_state = {
    'user': None
}


def register():
    while True:
        username = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        re_pwd = input('请确认密码：').strip()
        if pwd != re_pwd:
            print('两次输入密码不一致')
            continue
        flag, msg = student_interface.stu_register(username, pwd)
        if flag:
            print(msg)
            break  # 注册成功则退出循环
        else:
            print(msg)


def login():
    while True:
        username = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        flag, msg = common_interface.login(username, pwd, user_type='student')
        if flag:
            user_state['user'] = username  # 记录当前用户状态
            print(msg)
            break
        else:
            print(msg)


@common.auth('student')
def choose_campus():
    while True:
        # 获取学校列表
        flag, values = common_interface.get_all_campus()
        if not flag:  # 如果没有学校，则打印提示语
            print(values)
            break
        for index, campus_name in enumerate(values):
            print(f'编号：{index}  学校：{campus_name}')
        choice = input('请输入学校编号：').strip()
        if not choice.isdigit():
            print('请输入数字编号！')
            continue
        if int(choice) not in range(len(values)):
            print('请输入正确的编号！')
            continue
        # 获取选择的学校名称
        campus_name = values[int(choice)]
        msg = student_interface.add_campus_control(campus_name, user_state.get('user'))
        print(msg)
        break


def __get_course_name():
    '''
    获取学生课程
    :return: 返回选择的课程名称
    '''
    while True:
        # 获取学生所在学校的所有课程
        flag, values = student_interface.get_course_list(user_state.get('user'))
        if flag:
            for index, course in enumerate(values):
                print(f'课程编号：{index},课程：{course}')
            choice = input('请选择课程编号：')  # 让用户选择课程编号
            if not choice.isdigit():
                print('课程编号只能是数字')
                continue
            if int(choice) not in range(len(values)):
                print('请输入正确的课程编号')
                continue
            return values[int(choice)]


@common.auth('student')
def choose_course():
    while True:
        course_name = __get_course_name()
        if not course_name: break  # 没有课程则break
        # 传课程名称、学生名称
        flag, msg = student_interface.add_course_control(course_name, user_state.get('user'))
        if flag:
            print(msg)
            break
        else:
            print(msg)


@common.auth('student')
def select_score():
    print('请先输入查看分数的课程编号：')
    while True:
        course_name = __get_course_name()
        if not course_name:
            flag, score_dict = student_interface.stu_score_control(user_state.get('user'))
            if flag:
                for course, score in score_dict:
                    print(f'课程{course}成绩为：{score}')
                break
            else:
                print(score_dict)
                break

        flag, score = student_interface.stu_score_control(user_state.get('user'), course_name)
        if flag:
            print(f'{user_state.get("user")} 您的课程{course_name}分数为：{score}')
            break
        else:
            print(score)


func_dict = {
    '1': register,
    '2': login,
    '3': choose_campus,
    '4': choose_course,
    '5': select_score
}


def stu_view():
    while True:
        print(
            '''输入b返回上一层
            ★ 1.注册
            ★ 2.登录功能
            ★ 3.选择校区
            ★ 4.选择课程
            ★ 5.查看分数
        ''')
        choice = input('请输入服务编号：').strip()
        if choice == 'b':
            break
        if choice not in func_dict:
            print('输入有误，请重新输入')
            continue
        func_dict[choice]()
