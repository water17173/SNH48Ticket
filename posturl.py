#-*- coding: utf-8 -*- 
import requests,urllib
urllib.getproxies_registry = lambda : {}
cookies = 'your cookie'
#https://shop.48.cn/tickets/item/* 的cookie，×为门票编号

postheader = {'Accept':'application/json, text/javascript, */*; q=0.01',
           'Accept-Encoding':'gzip, deflate, sdch, br',
           'Accept-Language':'zh-CN,zh;q=0.8',
           'Connection':'keep-alive',
           'Content-Length':'56',
           'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
           'Cookie':cookies,
           'Host':'shop.48.cn',
           'Origin':'https://shop.48.cn',
           'Referer':'https://shop.48.cn/tickets/item/*',#*为门票编号
           'Referer':'https://shop.48.cn/tickets',
           'Upgrade-Insecure-Requests':'1',
           'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
           'X-Requested-With':'XMLHttpRequest'}

postData = {'id':'×','num':'1','seattype':'2','brand_id':'3','r':'0.3731131006391708'}
#id:门票编号，num:门票数量，seattype:门票类型,2为VIP，3为普座，4为站票，brand_id：团体编号(gnz48为3)，’r‘:随机数
if __name__ == '__main__':
    r = requests.session()
    res = r.get('https://shop.48.cn/tickets/item/*',headers = {'Cookie':cookies})#*为门票编号
    while 1:
        try:
            req = r.get('https://shop.48.cn/tickets/saleList?id=1022&brand_id=3')#查询库存，*为门票编号和团体编号
            req = eval(req.content.replace('true','1').replace('false','0'))
        except:
            traceback.print_exc()
            continue
        if req[1]['amount']:#*为票种，1为VIP，2为普座，3为站票
            content = r.post('https://shop.48.cn/TOrder/add',headers = postheader,data = postData)
            if content.status_code == 200:
                print '下单成功，请前往shop.snh48.com付款。
        else:continue

