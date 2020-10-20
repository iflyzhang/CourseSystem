# -*- coding: utf-8 -*-
"""
@file   : src.py
@author : Andy Zhang
@time   : 2020/10/15 14:40
@Desc   : 
"""
from core.student import stu_view
from core.teacher import teach_view
from core.admin import admin_view

func_dict = {
    '1': stu_view,
    '2': teach_view,
    '3': admin_view
}


def run():
    while True:
        # 打印字体加颜色书写格式：\033[显示方式;前景色;背景色m + 结尾部分：\033[0m
        print("\33[1;35;1m 欢迎进入选课系统 \33[0m".center(50, "#"), end='')
        print('''
            1.学生入口
            2.教师入口
            3.管理员入口
            4.【q】退出''')
        print("\33[1;35;1m end \33[0m".center(56, "#"))
        choice = input('请输入服务编号：').strip()
        if choice == 'q':
            break
        if choice not in func_dict:
            print('输入有误，请重新输入')
            continue
        func_dict[choice]()
