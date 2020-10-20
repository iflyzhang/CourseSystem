# -*- coding: utf-8 -*-
"""
@file   : teacher.py
@author : Andy Zhang
@time   : 2020/10/15 15:22
@Desc   : 
"""
from interface import teacher_interface
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
        flag, msg = teacher_interface.teach_register(username, pwd)
        if flag:
            print(msg)
            break  # 注册成功则退出循环
        else:
            print(msg)


def login():
    while True:
        username = input('请输入用户名：').strip()
        pwd = input('请输入密码：').strip()
        flag, msg = common_interface.login(username, pwd, user_type='teacher')
        if flag:
            user_state['user'] = username  # 记录当前用户状态
            print(msg)
            break
        else:
            print(msg)


# 查看课程
@common.auth('teacher')
def check_course():
    while True:
        course = teacher_interface.check_sourse_control(user_state.get('user'))
        if course:
            print(course)
        else:
            print('教师当前还没有课程信息')
        break


def __get_campus_name():
    '''
    获取校区名称
    :return:
    '''
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
        return values[int(choice)]


# 选择课程
@common.auth('teacher')
def add_course():
    campus_name = __get_campus_name()
    while True:
        # 获取学校下的课程
        course_list = common_interface.get_all_course_by_school(campus_name)
        if not course_list:
            print('该校区暂无课程，请联系管理员添加')
            break
        for index, course in enumerate(course_list):
            print(f'编号：{index}  课程：{course}')
        choice = input('请输入课程编号：').strip()
        if not choice.isdigit():
            print('请输入数字编号！')
            continue
        if int(choice) not in range(len(course_list)):
            print('请输入正确的编号！')
            continue
        # 获取选择的课程名称
        course_name = course_list[int(choice)]
        flag, msg = teacher_interface.add_course_control(course_name, user_state.get('user'))
        if flag:
            print(msg)
        else:
            print(msg)
        break


def __get_course_name_by_teacher():
    course_list = common_interface.get_all_course_by_teacher(user_state.get('user'))
    while True:
        if not course_list:
            print('你还没有课程，请先选择课程')
            break
        for index, course in enumerate(course_list):
            print(f'编号：{index}  课程：{course}')
        choice = input('请输入操作的课程编号：').strip()
        if not choice.isdigit():
            print('请输入数字编号！')
            continue
        if int(choice) not in range(len(course_list)):
            print('请输入正确的编号！')
            continue
        # 获取选择的课程名称
        return course_list[int(choice)]


# 查看学生
@common.auth('teacher')
def check_stu():
    print('请选择要看哪个课程的学生：')
    course_name = __get_course_name_by_teacher()
    while True:
        stu_list = common_interface.get_stu_list_by_course(course_name)
        if not stu_list:
            print('还没有学生选择该课程')
            break
        print(stu_list)
        break


# 修改分数
@common.auth('teacher')
def modify_score():
    course_name = __get_course_name_by_teacher()
    while True:
        stu_list = common_interface.get_stu_list_by_course(course_name)
        for index, stu in enumerate(stu_list):
            print(f'编号：{index}  学生：{stu}')
        choice = input('请输入要修改的学生编号：').strip()
        if not choice.isdigit():
            print('请输入数字编号！')
            continue
        if int(choice) not in range(len(stu_list)):
            print('请输入正确的编号！')
            continue
        mod_stu = stu_list[int(choice)]
        score = input('请输入学生分数:').strip()
        msg = teacher_interface.modify_score_control(user_state.get('user'),
                                                     mod_stu, course_name, score)
        print(msg)
        break


func_dict = {
    '1': login,
    '2': check_course,
    '3': add_course,
    '4': check_stu,
    '5': modify_score
}


def teach_view():
    while True:
        print(
            '''输入b返回上一层
            ★ 1.登录
            ★ 2.查看课程
            ★ 3.选择课程
            ★ 4.查看学生
            ★ 5.修改分数
        ''')
        choice = input(f'教师:{user_state.get("user")},请输入服务编号：').strip()
        if choice == 'b':
            break
        if choice not in func_dict:
            print('输入有误，请重新输入')
            continue
        func_dict[choice]()
