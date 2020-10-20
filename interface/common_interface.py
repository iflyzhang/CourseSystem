# -*- coding: utf-8 -*-
"""
@file   : common_interface.py
@author : Andy Zhang
@time   : 2020/10/18 11:00
@Desc   : 
"""
import os
from conf import settings
from db import models


def login(name, pwd, user_type):
    if user_type == 'admin':
        obj = models.Admin.select(name)
    elif user_type == 'student':
        obj = models.Student.select(name)
    elif user_type == 'teacher':
        obj = models.Teacher.select(name)
    else:
        return False, '登录角色不正确'
    if obj:  # 用户存在，则校验密码
        if pwd == obj.pwd:
            return True, f'用户{name}登录成功'
        else:
            return False, '密码错误'
    else:
        return False, '用户不存在'


def get_all_campus():
    '''
    获取当前所有学校
    :return:
    '''
    campus_dir = os.path.join(settings.DB_PATH, 'campus')
    if not os.path.exists(campus_dir):
        return False, '还没有学校，请先创建'
    campus_list = os.listdir(campus_dir)
    return True, campus_list  # 返回学校列表


def get_all_course_by_school(school):
    school_obj = models.Campus.select(school)
    if school_obj.course_list:
        return school_obj.course_list

def get_all_course_by_teacher(user):
    teach_obj = models.Teacher.select(user)
    return teach_obj.teacher_courses

def get_stu_list_by_course(course):
    course_obj = models.Course.select(course)
    return course_obj.students
