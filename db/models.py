# -*- coding: utf-8 -*-
"""
@file   : models.py
@author : Andy Zhang
@time   : 2020/10/15 14:46
@Desc   : 
"""

from db import db_handle


class Base:

    def save(self):
        db_handle.save_data(self)  # 将self对象保存

    @classmethod
    def select(cls, username):
        return db_handle.select_data(cls, username)


# 管理员
class Admin(Base):
    '''
    管理员类，包含创建校区、创建教师、创建课程方法
    '''

    def __init__(self, username, pwd):
        self.name = username
        self.pwd = pwd
        # self.save()  # 保存用户

    # 创建学校
    def create_campus(self, username, addr):
        '''
        创建学校
        :param username: 学校名称
        :param addr: 学校地址
        :return:
        '''
        school = Campus(username, addr)
        school.save()

    # 创建课程
    def create_course(self, campus_obj, course_name, course_price):
        '''
        创建课程
        :param campus_obj:课程所在校区
        :param course_name: 课程名称
        :param course_price: 价格
        :return:
        '''
        course = Course(course_name.lower(), course_price)  # 课程名称统一转小写
        course.save()  # 保存课程对象
        campus_obj.course_list.append(course.name)  # 学校的课程列表添加课程名称
        campus_obj.save()

    # 创建教师
    def create_teacher(self, name, pwd):
        '''
        创建教师
        :param name:教师名称
        :param pwd: 密码
        :return:
        '''
        teach_obj = Teacher(name, pwd)  # 创建教师对象
        teach_obj.save()


# 学生
class Student(Base):
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.campus = None  # 每次学生只有一个校区
        self.stu_course = []  # 学生课程列表
        self.payed = {}  # 是否已缴费{"course_name":True}
        self.score = {}  # 课程分数{"course_name":0}

    def add_campus(self, campus_name):
        '''
        学生添加学校
        :param campus_name: 学校名称
        :return:
        '''
        self.campus = campus_name
        self.save()

    def add_course(self, course):
        self.stu_course.append(course)
        self.save()
        course_obj = Course.select(course)
        course_obj.students.append(self.name)
        course_obj.save()


# 学校
class Campus(Base):
    def __init__(self, name, addr):
        self.name = name
        self.addr = addr
        self.course_list = []  # 学校课程列表


# 课程
class Course(Base):
    def __init__(self, couse_name, course_price):
        self.name = couse_name
        self.course_price = course_price
        self.students = []  # 学生列表


# 教师
class Teacher(Base):
    def __init__(self, name, pwd):
        self.name = name
        self.pwd = pwd
        self.teacher_courses = []  # 教师课程列表
        # self.campus = None  # 教师所属学校

    def add_course(self, course):
        self.teacher_courses.append(course)
        self.save()

    def modify_score(self, stu, course, num):
        '''
        修改学生分数方法
        :param stu: 学生名称
        :param course: 课程名称
        :param num: 分数
        :return:
        '''
        stu_obj = Student.select(stu)
        stu_obj.score[course] = num
        stu_obj.save()
