#coding=utf8

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import timezone

import httplib
import json

from models import user

single = [
          "name", #股票名称
          "today_start", #今日开盘价
          "yesterday_end", #昨日收盘价
          "current_price", #当前价格
          "today_highest", #今日最高价
          "today_lowest", #今日最低价
          "buy_price", #竞买价
          "sell_price", #竞卖价
          "deal_num", #成交的股票数
          "deal_cash", #成交金额
          "buy1_num", #买一股数
          "buy1_price", #买一报价
          "buy2_num", #买二股数
          "buy2_price", #买二报价
          "buy3_num", #买三股数
          "buy3_price", #买三报价
          "buy4_num", #买四股数
          "buy4_price", #买四报价
          "buy5_num", #买五股数
          "buy5_price", #买五报价
          "sell1_num", #卖一股数
          "sell1_price", #卖一报价
          "sell2_num", #买二股数
          "sell2_price", #卖二报价
          "sell3_num", #卖三股数
          "sell3_price", #卖三报价
          "sell4_num", #卖四股数
          "sell4_price", #卖四报价
          "sell5_num", #卖五股数
          "sell5_price", #卖五报价
          "date", #日期
          "time"] #时间

board = [
         "name", #指数名称
         "current_point", #当前点数
         "current_price", #当前价格
         "rate", #涨跌率
         "deal_num", #成交量（手）
         "deal_price", #成交额（万元）
         ]

import re

pattern = re.compile('var hq_str_(\w+)=\"(.+)\";\n')
def get_stock_info(code):
    conn = httplib.HTTPConnection("hq.sinajs.cn") 
    conn.request("GET","/list="+code)
    r = conn.getresponse()
    count = 0
    while r.status != 200:
        
        if count > 3 :
            return ""
        
        conn.request("GET","list="+code)
        r = conn.getresponse()
        
        count+=1
        
    ret = {}
    match = pattern.findall(r.read())
    for i in xrange(0,len(match)):
        arr = match[i][1].split(',')
        arr[0] = unicode(arr[0],"gbk")
        ret[match[i][0]] = arr
    return ret

def get_object(sets,param):
        objs = sets.filter(**param)
        if objs.count() == 0:
            return None
        else:
            return objs[0]
        
@csrf_exempt
def register(request,userid,pwd):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("fail")
    
    u = user(userid=userid,pwd=pwd,status=0,cash=100000,ip="",date_lastlogin=timezone.now(),date_create=timezone.now())
    u.save()
    return HttpResponse("ok")

@csrf_exempt
def login(request,userid,pwd):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("fail")
    
    u.date_lastlogin=timezone.now()
    u.save()
    return HttpResponse("ok")

@csrf_exempt
def info(request,code):
        
    return HttpResponse(json.dumps(get_stock_info(code)))

@csrf_exempt
def choosed(request,userid):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("")
    objs = u.watch_set.all()
    return HttpResponse(json.dumps(get_stock_info(",".join(["%s"%(objs[i].code) for i in xrange(0,len(objs))]))))

@csrf_exempt
def stocks(request,userid):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("")
    
    objs = u.stocks_set.all()
    datas = get_stock_info(",".join(["%s"%(objs[i].code) for i in xrange(0,len(objs))]))
    
    ret = {}
    
    for i in xrange(0,len(objs)):
        value = objs[i].num*datas[objs[i].code][3]
        total = objs[i].num*objs[i].price
        ret[objs[i].code] = [objs[i].num,objs[i].price,value,total,value-total,(value/total-1)*100] + datas[objs[i].code]
        
    return HttpResponse(json.dumps(ret))

@csrf_exempt
def watch(request,code,userid):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("")
    
    w = u.watch_set.create(code = code,date_create=timezone.now())
    w.save()
    return HttpResponse("ok")

@csrf_exempt
def buy(request,code,num,price,userid):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("")
    
    if num*price > u.cash:
        return HttpResponse("cash not enough")
    
    info = get_stock_info(code)
    if info == "":
        return HttpResponse("")
    
    rest = num
    for i in xrange(20,30,2):
        if info[i+1]<=price:
            rest -= info[i]
    
    if rest > 0:
        return HttpResponse("fail")
    
    b = get_object(u.stocks_set,{'code':code})
    if b == None:
        b = u.stocks_set.create(code = code,num=num,price=price,date_create=timezone.now())
    else:
        b.num += num
        b.price = (b.price + price)/2.0
    b.save()
    u.cash -= num*price
    u.save()
    return HttpResponse("ok")

@csrf_exempt
def sell(request,code,num,price,userid):
    u = get_object(user,{'userid':userid})
    if u == None:
        return HttpResponse("")
    
    b = get_object(u.stocks_set,{'code':code})
    if b == None or b.num < num:
        return HttpResponse("num not enough")
    
    info = get_stock_info(code)
    if info == "":
        return HttpResponse("")
    
    rest = num
    for i in xrange(20,30,2):
        if info[i+1]>=price:
            rest -= info[i]
    
    if rest > 0:
        return HttpResponse("fail")

    b.num -= num
    if b.num > 0:
        b.save()
    else:
        b.delete()
        
    u.cash += num*price
    return HttpResponse("ok")