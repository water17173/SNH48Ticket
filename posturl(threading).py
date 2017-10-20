# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from tkinter import *
import time
import requests
import urllib
import traceback
import threading
import json


class order(object):
    def __init__(self,user,password,ticketcode,seattype):
        self.user = user
        self.password = password
        self.ticketcode = ticketcode
        self.seattype = seattype
        self.cookies = ''
        self.req = requests.session()
        root = Tk()
        self.login()

    def login(self):
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
        self.cookies.strip(';')
        print self.cookies
        browser.quit()

    def ticket(self):
    	url = 'http://shop.48.cn'
    	res = self.req.get(url,headers = {'Cookie':self.cookies})
        postData = {'id': self.ticketcode, 'num': '1', 'seattype': self.seattype,'brand_id': '3', 'r': '0.3731131006391708'}  # id:门票编号，num:门票数量，seattype:门票类型,2为VIP，3为普座，4为站票，brand_id：团体编号(gnz48为3)，’r‘:随机数
        while 1:
	        try:
	            res = self.req.get(url)
	        except:
	            traceback.print_exc()
	            continue
	        if json.loads(res.content)[1]['amount']:  # *为票种，1为VIP，2为普座，3为站票
	            resp = self.req.post('https://shop.48.cn/TOrder/add',headers={'Cookie': self.cookies}, data=postData)
	            if resp.status_code == 200:
	                print '下单成功，请前往shop.snh48.com付款。'
	        else:
	            continue

if __name__ == '__main__':
	se = order('snh48042191478','yinheng1993','1426','2')  # id:门票编号，seattype:门票类型,2为VIP，3为普座，4为站票
	for i in range(30):
        th = threading.Thread(target=se.ticket)
        th.start()
