"""
>>> get_stock_info("s_sh000001")
"""

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import httplib

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
def get(code):
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


@csrf_exempt
def info(request,code):
        
    return HttpResponse("info %s" % get_stock_info(code))

@csrf_exempt
def choosed(request,userid):
    return HttpResponse("choosed")

@csrf_exempt
def stocks(request,userid):
    return HttpResponse("stocks")

@csrf_exempt
def watch(request,code,userid):
    return HttpResponse("watch %s" % (code))

@csrf_exempt
def buy(request,code,num,price,userid):
    return HttpResponse("buy")

@csrf_exempt
def sell(request,code,num,price,userid):
    return HttpResponse("sell")