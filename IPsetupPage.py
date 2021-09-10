#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter.messagebox import *
from LinkPage import *
import os
import socket


class IPSetupPage(object):
    def __init__(self, master=None):
        self.window = master  # 定义内部变量window
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.ip = StringVar()
        self.createPage()

    def createPage(self):
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Button(self.page, text='改为静态IP地址', command=self.IP_change_static).grid(row=1, stick=W, pady=10)
        Button(self.page, text='改为动态IP地址', command=self.IP_change_dynamic).grid(row=1, column=1, stick=E)
        Button(self.page, text='刷新当前IP地址', command=self.IP_get).grid(row=2, stick=W, pady=10)
        Label(self.page, text='当前IP地址:').grid(row=3, stick=E, pady=10)
        self.var = StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
        Label(self.page, textvariable=self.var).grid(row=3, column=1, stick=E)
        Button(self.page, text='下一步', command=self.IP_check).grid(row=4, column=1, stick=E)

    def IP_change_static(self):  # 改变IP地址为静态
        os.system("C:\\Users\95184\Desktop\IPstatic.bat")  # bat文件位置

    def IP_change_dynamic(self):  # 改变IP地址为动态
        os.system("C:\\Users\95184\Desktop\IPdynamic.bat ")  # bat文件位置

    def IP_get(self):
        # 获取计算机名称
        hostname = socket.gethostname()
        # 获取本机IP
        self.ip = socket.gethostbyname(hostname)
        self.var.set(self.ip)


    def IP_check(self):
        if socket.gethostbyname(socket.gethostname()) == '192.168.0.100':
            self.page.pack_forget()
            LinkPage(self.window)
        else:
            showinfo(title='错误', message='当前IP地址不为192.168.0.100')