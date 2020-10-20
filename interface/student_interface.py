# -*- coding: utf-8 -*-
"""
@file   : student_interface.py
@author : Andy Zhang
@time   : 2020/10/15 15:22
@Desc   : 
"""
from db.models import Student
from db import models
from lib import common


def stu_register(name, pwd):
    if Student.select(name):
        return False, '学生已存在'
    stu_obj = Student(name, pwd)
    stu_obj.save()
    return True, f'学生{name}注册成功'


def add_campus_control(campus_name, stu_name):
    stu_obj = models.Student.select(stu_name)
    if stu_obj.campus:
        return f'学生已有学校:{campus_name}'
    stu_obj.add_campus(campus_name)
    return f'学校{campus_name}添加成功'


def get_course_list(name):
    '''
    获取学生课程列表
    :param name:学生名称
    :return: 课程列表
    '''
    stu_obj = models.Student.select(name)
    stu_school = stu_obj.campus
    if not stu_school:
        return False, '你还没有校区，请先添加校区'
    campus_obj = models.Campus.select(stu_school)
    if not campus_obj.course_list:
        return False, f'你所在校区【{stu_school}】还没有课程。'
    return True, campus_obj.course_list  # 返回课程列表


def add_course_control(course, user):
    '''
    添加课程接口
    :param course: 课程名
    :param user: 需要添加课程的学生
    :return:
    '''
    stu_obj = models.Student.select(user)
    if course in stu_obj.stu_course:
        return False, f'课程{course}已存在'
    stu_obj.add_course(course)
    return True, f'恭喜，你所在的校区{stu_obj.campus}添加课程{course}成功'


def stu_score_control(user,course_name=''):
    stu_obj = models.Student.select(user)
    if not stu_obj.score: return False, '学生课程还没有分数'
    if not course_name:
        return True,stu_obj.score
    if course_name not in stu_obj.score: return False, '学生没有该课程分数信息'
    return True, stu_obj.score.get(course_name)
