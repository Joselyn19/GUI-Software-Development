#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter import *
import XPS_Q8_drivers
import sc10
import sys
from FileLoadPage import *
from IPsetupPage import *



class LinkPage(object):
    def __init__(self, master=None):
        self.window = master  # 定义内部变量root
        self.window.geometry('%dx%d' % (600, 400))  # 设置窗口大小
        self.createPage()

    def createPage(self):
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page).grid(row=0, stick=W)
        Button(self.page, text='连接SC10光快门控制器', command=self.SC10_link).grid(row=1, stick=W, pady=10)
        #Button(self.page, text='检查SC10运动控制器连接', command=self.IP_change_dynamic).grid(row=1, column=1, stick=E)
        Button(self.page, text='连接XPS-Q8运动控制器', command=self.XPS_link).grid(row=2, stick=W, pady=10)
        Button(self.page, text='检查XPS-Q8运动控制器连接', command=self.XPS_check).grid(row=2, column=1, stick=E)
        #Button(self.page, text='刷新当前IP地址', command=self.IP_get).grid(row=2, stick=W, pady=10)
        #Label(self.page, text='当前IP地址:').grid(row=3, stick=E, pady=10)
        #self.var = StringVar()  # 将label标签的内容设置为字符类型，用var来接收hit_me函数的传出内容用以显示在标签上
        #Label(self.page, textvariable=self.var).grid(row=3, column=1, stick=E)
        Button(self.page, text='上一步', command=self.last_page).grid(row=4, stick=W, pady=10)
        Button(self.page, text='下一步', command=self.next_page).grid(row=4, column=1, stick=E)

    def SC10_link(self):
        # 连接SC10
        self.sc = sc10.SC10()
        # 如果光开关打开则关闭
        try:
            self.sc.closeShutter()
        except:
            pass

    def XPS_link(self):
        self.myxps = XPS_Q8_drivers.XPS()
        # 连接XPS
        self.socketId = self.myxps.TCP_ConnectToServer('192.168.0.254', 5001, 30)  # 主机连接器 ip端口号5001,30s后超时

    def XPS_check(self):
        if self.socketId == -1:
            showinfo(title='错误', message='连接XPS-Q8运动控制器失败，请检查IP地址及端口')
            self.sys.exit()
        else:
            showinfo(title='成功', message='连接XPS-Q8运动控制器成功')

    # 设定XPS运动控制器的通信错误类型返回函数
    def ErrorAndClose(self,socketId, errorCode, APIName):  # 返回0时无错误
        if (errorCode != -2) and (errorCode != -108):
            [errorCode2, errorString] = self.myxps.ErrorStringGet(socketId, errorCode)
            if errorCode2 != 0:
                print(APIName + ': ERROR ' + str(errorCode))
            else:
                print(APIName + ': ' + errorString)
        else:
            if errorCode == -2:  # 返回2时错误
                print(APIName + ': TCP timeout')
            if errorCode == -108:  # 返回108时错误
                print(APIName + ': The TCP/IP connection was closed by an administrator')
        myxps.TCP_CloseSocket(socketId)
        return

    def last_page(self):
        self.page.destroy()
        IPSetupPage(self.window)

    def next_page(self):
        #if self.stockId != -1 and #SC10连接成功：
            self.page.destroy()
            fileloadPage(self.window)
        #else：
            #showinfo(title='错误', message='SC10或XPS-Q8连接失败')