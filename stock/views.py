"""
>>> get_stock_info("s_sh000001")
"""

from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

import httplib

single = [
          "name", #��Ʊ����
          "today_start", #���տ��̼�
          "yesterday_end", #�������̼�
          "current_price", #��ǰ�۸�
          "today_highest", #������߼�
          "today_lowest", #������ͼ�
          "buy_price", #�����
          "sell_price", #������
          "deal_num", #�ɽ��Ĺ�Ʊ��
          "deal_cash", #�ɽ����
          "buy1_num", #��һ����
          "buy1_price", #��һ����
          "buy2_num", #�������
          "buy2_price", #�������
          "buy3_num", #��������
          "buy3_price", #��������
          "buy4_num", #���Ĺ���
          "buy4_price", #���ı���
          "buy5_num", #�������
          "buy5_price", #���屨��
          "sell1_num", #��һ����
          "sell1_price", #��һ����
          "sell2_num", #�������
          "sell2_price", #��������
          "sell3_num", #��������
          "sell3_price", #��������
          "sell4_num", #���Ĺ���
          "sell4_price", #���ı���
          "sell5_num", #�������
          "sell5_price", #���屨��
          "date", #����
          "time"] #ʱ��

board = [
         "name", #ָ������
         "current_point", #��ǰ����
         "current_price", #��ǰ�۸�
         "rate", #�ǵ���
         "deal_num", #�ɽ������֣�
         "deal_price", #�ɽ����Ԫ��
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