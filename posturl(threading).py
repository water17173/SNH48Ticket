# -*- coding: utf-8 -*-
import requests
import urllib
import traceback
import threading
import time

urllib.getproxies_registry = lambda: {}
cookies = 'pgv_pvi=7556883456; tencentSig=402739200; SessionID=t0m5b4o2lc4lcnhhrjy25akt; uchome_auth=4b293ApRGj8bEcgeMWYJmtYhOOrX6rZp7R6uMRfsLIafQ5Q60PIftxsWIGreUI0oYVISDA7%2FVI5tyEiQdmb%2B9Q2Mvpm%2B; uchome_loginuser=snh48042191478; _qddaz=QD.3y0tur.nm7q1u.itg1oy5r; route=1777915d2532482d4588d5ef37a84c06; .AspNet.ApplicationCookie=jwo4x2ENNotfocMk6xw54iS4LEQNydjvoda4g-jkk4LgkTiwqxkd42Ne0auh0Pfgen78mFVotb62j45BonjPEgoNt-c1NkSxEL2b-iafFdrJkM7stSMiWvjKaHnTbIzti0UKQHuyhAGMPSylsgRO_QnKBxnU1PRd_sqJpOXyd5PArvE2U7884VUQojFpq5P_s4WxHdtNQ1KbOX2c7GxuWto4JNnpl00T9kYTmgKhXRAkwc417pvXPJdXmOWDLaqxKD-D5svenaivkfvZFcgm-yESlDfTe7ky9_0J1F3SY4NgGWvCXeMWSdSG6oHllI4L7NmlEQK4O_NesiektDRyDPdMtx3CaJR3SQC5NRUwMtVBz86dZ0KIZ2J3uoDTA_EUPUp3D4MKX0pNIWSDE-VNEvd8KyNucA7c6bvEsU2db9i4k4NzfBUfc0C97I9GMOomTxPY7hjSQtKpbI_tKqiKyXeJ0_ypu4OeOzMwdZaeyJRnZnc6S40PHzvUozdkIH3zHJyELQoMOB0xR2ijLcH9PXI3T61yYgDukZZ2ZtZGvsOdeUkAl8nzImxkBUNBdNn5vC8eL285LbSnkaj-oAJzDjPZvuNd92w4xtL1sGOEGGdx_Wpwz9TZqp0YKuCB04NQ; __RequestVerificationToken=3wgO5X17g7ZE95S243pj1BX42d80lCYJmSVtPUC52PLJ2Opcx36gAozs768rwiBtzgr6Tr7jQStZP-WfSSvvNF_QgxDkhlP2qZEMo-C3wxc1'
# https://shop.48.cn/tickets/item/* 的cookie，×为门票编号

postheader = {'Accept': 'application/json, text/javascript, */*; q=0.01',
              'Accept-Encoding': 'gzip, deflate, sdch, br',
              'Accept-Language': 'zh-CN,zh;q=0.8',
              'Connection': 'keep-alive',
              'Content-Length': '56',
              'Content-Type': 'application/x-www-form-urlencoded; \
               charset=UTF-8',
              'Cookie': cookies,
              'Host': 'shop.48.cn',
              'Origin': 'https://shop.48.cn',
              'Referer': 'https://shop.48.cn/tickets/item/1022',  # *为门票编号
              'Referer': 'https://shop.48.cn/tickets',
              'Upgrade-Insecure-Requests': '1',
              'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
              AppleWebKit/537.36 (KHTML, like Gecko) \
              Chrome/58.0.3029.110 Safari/537.36',
              'X-Requested-With': 'XMLHttpRequest'}

postData = {'id': '1022', 'num': '1', 'seattype': '2',
            'brand_id': '3', 'r': '0.3731131006391708'}
# id:门票编号，num:门票数量，seattype:门票类型,2为VIP，3为普座，4为站票，brand_id：团体编号(gnz48为3)，’r‘:随机数
def tickets(url,r):
    while 1:
        try:
            req = r.get(url)
            req = eval(req.content.replace('true', '1').replace('false', '0'))
        except:
            traceback.print_exc()
            continue
        # print req[1]['amount']
        if req[1]['amount']:  # *为票种，1为VIP，2为普座，3为站票
            content = r.post('https://shop.48.cn/TOrder/add',
                           headers=postheader, data=postData)
          if content.status_code == 200:
              print '下单成功，请前往shop.snh48.com付款。'
        else:
            continue

if __name__ == '__main__':
    r = requests.session()
    res = r.get('https://shop.48.cn/tickets/item/1022',
                headers={'Cookie': cookies})  # *为门票编号
    url = 'https://shop.48.cn/tickets/saleList?id=1022&brand_id=3'
    # ts = []
    start = time.clock()
    for i in range(15):
        th = threading.Thread(target=tickets,args = [url,r])
        th.start()
    #     ts.append(th)
    
    # for i in ts:
    #     i.join()

    
    # end = time.clock()
    # print end-start
    # start = time.clock()
    # for i in range(50):
    #     tickets(url,r)
    # end = time.clock()
    # print end-start
    # 
