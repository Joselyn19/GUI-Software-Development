#!/usr/bin/env python
# -*- coding: utf-8 -*-

from tkinter.messagebox import *
import tkinter.filedialog
from tkinter import*
import os
import socket
import webbrowser
from ftplib import FTP
import XPS_Q8_drivers
import sc10
import sys
import time



class IPSetupPage(object):# IP地址修改页面
    def __init__(self, master=None):# 页面初始化
        self.window = master  # 定义内部变量window
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.ip = StringVar()
        self.createPage()

    def createPage(self): # 规划页面
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page, text='修改IP地址', font=12, fg='red').grid(row=0,columnspan=3)
        Label(self.page, text='修改IP地址:').grid(row=1, stick=E, pady=5)
        Button(self.page, text='改为静态', command=self.IP_change_static).grid(row=1, column=1, padx=20)
        Button(self.page, text='改为动态', command=self.IP_change_dynamic).grid(row=1, column=2)
        Label(self.page, text='当前IP地址:').grid(row=2, stick=E, pady=0)
        self.currentip = StringVar()  # 将label标签的内容设置为字符类型，用var来接收
        #hit_me函数的传出内容用以显示在标签上
        Label(self.page, textvariable=self.currentip).grid(row=2, column=1, stick=W)
        Button(self.page, text='刷新IP地址', command=self.IP_get).grid(row=2, column=2, stick=E, pady=10)
        Button(self.page, text='下一步', command=self.IP_check).grid(row=4, column=2, stick=E)
        Label(self.page, text='说明：静态IP地址：192.168.0.100，子网掩码：255.255.255.0').grid(row=5, columnspan=3, pady=20)

    def IP_change_static(self):  # 改变IP地址为静态
        os.system("C:\\Users\95184\Desktop\IPstatic.bat")  # bat文件位置

    def IP_change_dynamic(self):  # 改变IP地址为动态
        os.system("C:\\Users\95184\Desktop\IPdynamic.bat ")  # bat文件位置

    def IP_get(self):# 获得当前IP地址
        # 获取计算机名称
        hostname = socket.gethostname()
        # 获取本机IP
        self.ip = socket.gethostbyname(hostname)
        self.currentip.set(self.ip)

    def IP_check(self): #进入下一页
        #if socket.gethostbyname(socket.gethostname()) == '192.168.0.100':
            self.page.pack_forget()
            SetControllerPage(self.window)
        #else:
            #showinfo(title='错误', message='当前IP地址不为192.168.0.100')

class SetControllerPage(object):# 运动控制器配置页面
    def __init__(self, master=None):# 页面初始化
        self.window = master  # 定义内部变量window
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.createPage()

    def createPage(self):# 规划页面
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page, text='配置控制器', font=12, fg='red').grid(row=0,columnspan=2)
        Label(self.page, text='请登录http://192.198.0.254配置控制器').grid(row=2,columnspan=2,  pady=5)
        Button(self.page, text='打开浏览器', command=self.open_website).grid(row=3,columnspan=2,  pady=5)
        Button(self.page, text='上一步', command=self.last_page).grid(row=4, stick=W, pady=5)
        Button(self.page, text='下一步', command=self.next_page).grid(row=4, column=1, stick=E)

    def open_website(self):# 打开网页http://192.198.0.254
        webbrowser.open("http://192.198.0.254")

    def last_page(self):# 返回上一页
        self.page.destroy()
        IPSetupPage(self.window)

    def next_page(self):# 进入下一页
        self.page.destroy()
        FileLoadPage(self.window)

class FileLoadPage(object):# 轨迹文件上传页面
    def __init__(self, master=None):# 页面初始化
        self.window = master  # 定义内部变量window
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.Flag = False
        self.filelocalpath = ''
        self.createPage()
        self.ftp=None

    def createPage(self):# 规划页面
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page, text='上传轨迹文件至FTP服务器', font=12, fg='red').grid(row=0,columnspan=2)
        Label(self.page, text='用户名：').grid(row=1, stick=E, pady=5)
        self.username = Entry(self.page)
        self.username.grid(row=1, column=1)
        Label(self.page, text='密码：').grid(row=2, stick=E, pady=5)
        self.password = Entry(self.page,show='*')
        self.password.grid(row=2, column=1)
        Button(self.page, text='连接FTP服务器', command=self.ftp_connect).grid(row=3, pady=5)
        Button(self.page, text='断开与FTP服务器连接', command=self.ftp_disconnect).grid(row=3, column=1)
        Label(self.page, text='FTP服务器连接状态:').grid(row=4, stick=E, pady=5)
        self.LinkeState = StringVar()
        self.LinkeState.set('断开')
        Label(self.page, textvariable= self.LinkeState).grid(row=4, column=1, stick=W)
        Button(self.page, text='选择需要上传的文件', command=self.file_choose).grid(row=5, stick=W, pady=5)
        self.var1= StringVar()
        self.var1.set('您没有选择任何文件')
        Label(self.page, textvariable=self.var1).grid(row=5, column=1, stick=E)
        Button(self.page, text='上传文件至FTP服务端', command=self.file_upload).grid(row=6, stick=W, pady=5)
        Button(self.page, text='上一步', command=self.last_page).grid(row=7, stick=W,pady=5)
        Button(self.page, text='下一步', command=self.next_page).grid(row=7, column=1, stick=E)

    def file_choose(self):# 选择文件
        self.filelocalpath = tkinter.filedialog.askopenfilename()
        if self.filelocalpath != '':
            self.var1.set("您选择的文件是：" + self.filelocalpath)
        else:
            self.var1.set("您没有选择任何文件")

    def ftp_connect(self):# 连接FTP服务器
        if self.Flag == False:
            self.ftp = FTP()
            try: self.ftp.connect('192.168.0.254') # 连接
            except: showinfo(title='错误', message='FTP服务器连接失败，请检查IP设置')
            else:
                try: self.ftp.login(self.username.get(), self.password.get())  
                except: showinfo(title='错误', message='用户名或密码错误')
                else:
                    self.LinkeState.set('连接')
                    self.Flag = True
        else: showinfo(title='提示', message='FTP服务器已连接')

    def ftp_disconnect(self):# 断开FTP服务器
        if self.Flag == True:
            self.ftp.quit()
            self.LinkeState.set('断开')
            self.Flag = False
        else:
            showinfo(title='提示', message='FTP服务器连接已断开')

    def file_upload(self):# 轨迹文件上传
        if self.Flag == False:
            showinfo(title='提示', message='请连接FTP服务器')
        elif self.filelocalpath != '':
            self.bufsize = 1024     #设置缓冲块大小
            self.fp = open(self.filelocalpath, 'rb')     #以读模式在本地打开文件
            self.ftp.storbinary('STOR ' + '/Public/Trajactories', self.fp, self.bufsize)# 上传文件
            self.ftp.set_debuglevel(0)   #关闭调试
            self.fp.close()    #关闭文件
        else:
            showinfo(title='提示',message = '您没有选择任何文件')

    def last_page(self):# 返回上一页
        if self.Flag == False :
            self.page.destroy()
            SetControllerPage(self.window)
        else:
            showinfo(title='错误', message='请断开与FTP服务器连接')

    def next_page(self):# 进入下一页
        if self.Flag == False:
            self.page.destroy()
            LinkPage(self.window)
        else:
            showinfo(title='错误', message='请断开与FTP服务器连接')

class LinkPage(object):# 控制器连接页面
    def __init__(self, master=None, socketId=-1, myxps=None, sc=None):# 页面初始化
        self.window = master  # 定义内部变量root
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.socketId = socketId
        self.myxps = myxps
        self.sc = sc
        self.SC10Flag = False
        self.createPage()

    def createPage(self):# 规划页面
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page, text='建立控制连接', font=12, fg='red').grid(row=0,columnspan=3)
        Label(self.page, text='SC10光快门控制器：').grid(row=1, stick=E, pady=5)
        Button(self.page, text='测试', command=self.SC10_link).grid(row=1, column=1, padx=20)
        self.LinkStateSC10 = StringVar()
        self.LinkStateSC10.set('SC10连接未测试')
        Label(self.page, textvariable=self.LinkStateSC10).grid(row=2, columnspan=3)
        Label(self.page, text='XPS-Q8运动控制器：').grid(row=3, stick=E, pady=5)
        Button(self.page, text='连接', command=self.XPS_link).grid(row=3, column=1, padx=20)
        Button(self.page, text='断开', command=self.XPS_link_break).grid(row=3, column=2)
        self.LinkStateXPS = StringVar()
        self.LinkStateXPS.set('XPS-Q8连接状态：未连接')
        Label(self.page, textvariable=self.LinkStateXPS).grid(row=4, columnspan=3)
        Button(self.page, text='上一步', command=self.last_page).grid(row=5, stick=W, pady=10)
        Button(self.page, text='下一步', command=self.next_page).grid(row=5, column=2, stick=E)

    def SC10_link(self):# 测试SC10光快门控制器连接
        try:
            self.sc = sc10.SC10()
        except:
            showinfo(title='错误', message='连接SC10光快门控制器失败，请检查设备是否开启')
            self.LinkStateSC10.set('SC10连接测试未成功')
        else:
            self.SC10Flag = True
            self.LinkStateSC10.set('SC10连接测试成功')

    def XPS_link(self):# 连接XPS运动控制器
        if self.socketId != -1:
            showinfo(title='提示',message='XPS-Q8运动控制器已连接')
        else:
            self.myxps = XPS_Q8_drivers.XPS() # 连接XPS，创建实例
            self.socketId = self.myxps.TCP_ConnectToServer('192.168.0.254', 5001, 30)  
            if self.socketId == -1 :
                showinfo(title='错误', 
                message='连接XPS-Q8运动控制器失败，请检查IP地址及端口')
            else:
                showinfo(title='成功', message='连接XPS-Q8运动控制器成功')
                self.LinkStateXPS.set('XPS连接状态：已连接')

    def XPS_link_break(self):# 断开XPS运动控制器
        if self.socketId == -1 :
            showinfo(title='错误', message='XPS-Q8运动控制器未连接')
        else:
            self.myxps.TCP_CloseSocket(self.socketId)
            self.socketId = -1
            self.LinkStateXPS.set('XPS连接状态：未连接')

    def last_page(self):# 返回上一页
        if self.socketId != -1:
            showinfo(title='提示', message='请断开XPS-Q8连接')
        else:
            self.page.destroy()
            FileLoadPage(self.window)

    def next_page(self):# 进入下一页
        #if self.socketId != -1 and self.SC10Flag == True：
        self.page.destroy()
        ControlPage(self.window, self.socketId, self.myxps, self.sc)
        #else：
            #showinfo(title='错误', message='SC10未测试或XPS-Q8未连接')

class ControlPage(object):# 运动控制页面
    # 页面初始化    
    def __init__(self, master=None, socketId=-1, myxps=None, sc=None,  group='XY'):
        self.window = master  # 定义内部变量root
        self.window.geometry('%dx%d' % (500, 300))  # 设置窗口大小
        self.socketId = socketId
        self.myxps = myxps
        self.sc =sc
        self.group = group
        self.shutterstate = False
        self.createPage()
        self.errorCode=None

    def createPage(self):# 规划页面
        self.page = Frame(self.window)  # 创建Frame
        self.page.pack()
        Label(self.page, text='运动控制', font=12, fg='red').grid(row=0, columnspan=3)
        Label(self.page, text='定义运动类型:').grid(row=1, stick=E, pady=5)
        self.g = StringVar()
        self.g.set('XY')
        self.group='XY'
        Radiobutton(self.page, text='XY分组', variable=self.g, value='XY',command=self.group_XY).grid(row=1,column=1)
        Radiobutton(self.page, text='XYZ分组', variable=self.g, value='XYZ', command=self.group_XYZ).grid(row=1, column=2)
        #Button(self.page, text='ces', command=self.test).grid(row=2, stick=W)
        Label(self.page, text='光快门状态:').grid(row=3, stick=E, pady=5)
        self.shutter = StringVar()
        self.shutter.set('关')
        Radiobutton(self.page, text='关', variable=self.shutter, value='关',command=self.shutter_close).grid(row=3,column=1)
        Radiobutton(self.page, text='开', variable=self.shutter, value='开',command=self.shutter_open).grid(row=3, column=2)
        Label(self.page, text='轨迹文件选择:').grid(row=4, stick=E, pady=5)
        self.file = Entry(self.page)
        self.file.grid(row=4, column=1, stick=E)
        Label(self.page, text='移动速度(mm/s):').grid(row=5, stick=E, pady=5)
        self.velocity = Entry(self.page)
        self.velocity.grid(row=5, column=1, stick=W)
        Label(self.page, text='移动加速度(mm/s^2):').grid(row=6, stick=E, pady=5)
        self.accelerate = Entry(self.page)
        self.accelerate.grid(row=6, column=1, stick=W)
        Label(self.page, text='当前运动位置：').grid(row=7, stick=E, pady=5)
        self.position = StringVar()
        self.position.set('')
        Label(self.page, textvariable=self.position).grid(row=7, stick=W)
        Button(self.page, text='刷新', command=self.position_find).grid(row=7, column=2, stick=W)
        Button(self.page, text='上一步', command=self.last_page).grid(row=8, stick=W)
        Button(self.page, text='运行', command=self.move).grid(row=8, column=2, stick=E, pady=5)

    def group_XY(self):# 选择XY分组
        self.group='XY'
        self.positioner1 = self.group + '.X'
        self.positioner2 = self.group + '.Y'

    def group_XYZ(self):# 选择XYZ分组
        self.group='XYZ'
        self.positioner1 = self.group + '.X'
        self.positioner2 = self.group + '.Y'
        self.positioner3 = 'S' + '.Pos'

    def shutter_open(self):# 光快门打开
        self.shutterstate = True

    def shutter_close(self):# 光快门关闭
        self.shutterstate = False

    def move(self):# 运动控制器移动
        if self.sc==None:
            showinfo(title='错误',message='光快门未连接，请返回上一页连接光快门')
            return
        else:
            time.sleep(3)  # 延迟3s
            if self.shutterstate :
                self.sc.openShutter()  # 打开光开关
            else:
                self.sc.closeShutter()
            time.sleep(1)  # 延迟1s

        if self.myxps==None:
            showinfo(title='错误',message='XPS-Q8未连接，请返回上一页连接XPS-Q8')
            return
        else:
            # 运行轨迹文件Arc1.trj.txt 运动速度0.1单位/s 开始加速度1单位/s 运动次数5次
            [self.errorCode, returnString] = self.myxps.XYLineArcExecution(self.socketId, self.group, self.file.get(), self.velocity.get(), self.accelerate.get(), 5)  # 运行轨迹文件
            if self.errorCode != 0:
                self.ErrorAndClose(self.socketId, self.errorCode, 'XYLineArcExecution')

    # 设定XPS运动控制器的通信错误类型返回函数
    def ErrorAndClose(self, socketId, errorCode, APIName): 
        if (errorCode != -2) and (errorCode != -108):
            [errorCode2, errorString] = self.myxps.ErrorStringGet(socketId, errorCode)
            if errorCode2 != 0:
                showinfo(title='错误', message=APIName + ': ERROR ' + str(errorCode))
            else:
                showinfo(title='错误',message=APIName + ': ' + errorString)
        else:
            if errorCode == -2:  # 返回2时错误
                showinfo(title='错误', message=APIName + ': TCP超时')
            if errorCode == -108:  # 返回108时错误
                showinfo(title='错误', message=APIName + ': TCP/IP连接被管理员关闭')
        self.myxps.TCP_CloseSocket(socketId)
        #出现错误时断开与XPS连接，重新连接需要返回上一步
        return

    def position_find(self):# 显示当前坐标
        if self.myxps==None:
            showinfo(title='错误',message='XPS-Q8未连接，请返回上一页连接XPS-Q8')
            return
        else:
            [errorCode1, currentPosition1] = self.myxps.GroupPositionCurrentGet(self.socketId, self.positioner1, 1)
            if errorCode1 != 0:
                self.ErrorAndClose(self.socketId, errorCode1, 'GroupPositionCurrentGet')
                showinfo(title='错误',message='X轴坐标读取失败')
                return
            else:
                [errorCode2, currentPosition2] = self.myxps.GroupPositionCurrentGet(self.socketId, self.positioner2, 1)
                if errorCode2 != 0:
                    self.ErrorAndClose(self.socketId, errorCode2, 'GroupPositionCurrentGet')
                    showinfo(title='错误', message='Y轴坐标读取失败')
                    return
            if self.group == 'XY':
                self.position.set('X:'+str(currentPosition1)+'Y:'+str(currentPosition2))
                return
            else:
                [errorCode3, currentPosition3] = self.myxps.GroupPositionCurrentGet(self.socketId, self.positioner3, 1)
                if errorCode3 != 0:
                    self.ErrorAndClose(self.socketId,errorCode3, 'GroupPositionCurrentGet')
                    showinfo(title='错误', message='Z轴坐标读取失败')
                    return
                else:
                    self.position.set('X:' + str(currentPosition1) + 'Y:' + str(currentPosition2)+'Z:' + str(currentPosition3))
                    return

    def last_page(self):# 返回上一页
        self.page.destroy()
        LinkPage(self.window,self.socketId, self.myxps, self.sc)

window = tkinter.Tk()
window.title('飞秒激光加工平台控制软件')
IPSetupPage(window)
window.mainloop()

