#-*- coding: utf-8 -*- 
import requests

cookies = 'your cookie'#https://shop.48.cn/tickets/item/1006 的cookie

postheader = {'Accept':'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding':'gzip, deflate, sdch, br',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Connection':'keep-alive',
           'Content-Length':'56',
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'Cookie':cookies,
           'Host':'shop.48.cn',
           'Origin':'https://shop.48.cn',
           'Referer':'https://shop.48.cn/tickets/item/1006',#1006为门票编号
           'Referer':'https://shop.48.cn/tickets',
           'Upgrade-Insecure-Requests':'1',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
           'X-Requested-With':'XMLHttpRequest'}

postData = {'id':'1006','num':'1','seattype':'3','brand_id':'3','r':'0.3731131006391708'}
#id:门票编号，num:门票数量，seattype:门票类型2为VIP，3为普座，4为站票，brand_id：未知，’r‘:随机数
if __name__ == '__main__':
    r = requests.session()
    content = r.post('https://shop.48.cn/TOrder/add',headers = postheader,data = postData)
    print content.status_code


