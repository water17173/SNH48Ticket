# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
from bs4 import BeautifulSoup
import time
import requests
import urllib
import traceback
import threading
import json



class ORDER(object):
    def __init__(self):
        self.cookies = ''
        self.req = requests.session()
        self.root = Tk()
        self.root.title("snh48ticket")
        self.root.geometry('280x350')          
        self.root.resizable(width=False, height=False)
        self.frm = Frame(self.root)
        self.frm_L = Frame(self.frm)
        Label(self.frm_L, text='切票种类', font=('微软雅黑', 15),width = 9).pack(side=TOP)
        self.var3 = StringVar()
        self.var4 = StringVar()
        self.lb = Listbox(self.frm_L,  width = 11,height = 3,listvariable = self.var3)
        for item in ['VIP','普通坐票','站票']:
            self.lb.insert(END, item)
        self.lb.bind('<ButtonRelease-1>', self.print_item)
        self.lb.pack()
        Label(self.frm_L, text='门票编号', font=('微软雅黑', 15)).pack(side=TOP)
        Entry(self.frm_L, width = 11,textvariable = self.var4).pack()
        self.frm_L.pack(side=LEFT)

        self.frm_R = Frame(self.frm)
        Label(self.frm_R, text='账号', font=('微软雅黑', 15)).pack()
        self.var1 = StringVar()
        self.var2 = StringVar()

        Entry(self.frm_R, textvariable = self.var1,width = 15).pack()
        Label(self.frm_R, text='密码', font=('微软雅黑', 15)).pack()
        Entry(self.frm_R, textvariable = self.var2,width = 15).pack()
        Button(self.frm_R, text="开始捡漏", font=('微软雅黑', 12),height = 1,command = self.login).pack()
        self.frm_R.pack(side=RIGHT)


        self.t = Text(self.root,width = 28,height = 10,font=('微软雅黑', 10))
        self.t.insert(1.0, '欢迎使用切票器，请输入相关信息！\n')
        self.t.pack()

        self.frm.pack()
        self.root.mainloop()


    def loginstr(self,strings):
        self.t.insert(END, time.strftime('%H:%M:%S',time.localtime(time.time())) + '\t' + strings +'\n')

    def printmessage(self):
        self.t.insert(END, time.strftime('%H:%M:%S',time.localtime(time.time())) + '\t' + self.var1.get()+'\n')

    def print_item(self,event):
        self.seattype = self.lb.get(self.lb.curselection())

    def login(self):
        try:
            self.loginstr('登录中...')
            self.user = self.var1.get()
            self.password = self.var2.get()
            browser = webdriver.Chrome()
            browser.maximize_window()
            browser.implicitly_wait(10)
            browser.set_page_load_timeout(30)
            browser.get('http://vip.48.cn/Home/Login/index.html')
            browser.find_element_by_id('login').click()
            browser.find_element_by_id('username').send_keys(self.user)
            browser.find_element_by_id('password').send_keys(self.password)
            browser.find_element_by_id('submit').click()
            browser.find_element_by_link_text('SNH48 GROUP官方商城').click()
            browser.switch_to_window(browser.window_handles[-1])
            for i in browser.get_cookies():
                self.cookies += i['name']
                self.cookies += '='
                self.cookies += i['value']
                self.cookies += '; '
            print self.cookies
            browser.quit()
            self.loginstr('登录成功...')
            self.thread()
        except:
            self.loginstr('登录失败,请检查账号密码和网络环境...')

    def thread(self):
        self.ticketcode = self.var4.get()
        print self.ticketcode,self.seattype
        dict_change = {'VIP':'2','普通坐票':'3','站票':'4'}
        self.seattype = dict_change[self.seattype.encode('utf-8')]
        self.loginstr('开始捡漏...')
        for i in range(30):
            th = threading.Thread(target=self.ticket)
            th.start()
        self.loginstr('已开启30线程...')

    def ticket(self):
    	url = 'http://shop.48.cn'
    	res = self.req.get(url,headers = {'Cookie':self.cookies})
        postData = {'id': self.ticketcode, 'num': '1', 'seattype': self.seattype,'brand_id': '3', 'r': '0.3731131006391708'}  # id:门票编号，num:门票数量，seattype:门票类型,2为VIP，3为普座，4为站票，brand_id：团体编号(gnz48为3)，’r‘:随机数
        url = 'https://shop.48.cn/tickets/saleList?id={}&brand_id=3'.format(self.ticketcode)
        types = int(self.seattype) - 1
        times = 0
        while 1:
            try:
                res = self.req.get(url)
                times += 1
            except:
                traceback.print_exc()
                continue
            if json.loads(res.content)[types]['amount']:
                resp = self.req.post('https://shop.48.cn/TOrder/add',headers={'Cookie': self.cookies}, data=postData)     
            else:
                if times%1000 == 0:
                    soup = BeautifulSoup(requests.get('https://shop.48.cn/TOrder',headers={'Cookie':self.cookies}).content,'html.parser')
                    for  i in soup.find_all('a'):
                        if self.ticketcode in i.get('href'):
                            self.loginstr('切票成功，请前往shop.48.cn付款...')
                continue

if __name__ == '__main__':
	se = ORDER()
