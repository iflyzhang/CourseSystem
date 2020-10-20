# -*- coding: utf-8 -*-
"""
@file   : teacher_interface.py
@author : Andy Zhang
@time   : 2020/10/15 15:22
@Desc   : 
"""
from db import models


def teach_register(name, pwd):
    if models.Teacher.select(name):
        return False, '教师已存在'
    teach_obj = models.Teacher(name, pwd)
    teach_obj.save()
    return True, f'教师{name}注册成功'


def check_sourse_control(user):
    teach_obj = models.Teacher.select(user)
    if teach_obj.teacher_courses:
        return teach_obj.teacher_courses


def add_course_control(course, user):
    teach_obj = models.Teacher.select(user)
    if course in teach_obj.teacher_courses:
        return False, '课程已存在'
    teach_obj.add_course(course)
    return True, f'课程{course}添加成功'


def modify_score_control(teacher, stu, course, num):
    teach_obj = models.Teacher.select(teacher)
    teach_obj.modify_score(stu, course, num)
    return f'学生{stu}的课程{course}修改成功，修改后的分数为：{num}'
