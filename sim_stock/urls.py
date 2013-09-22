from django.conf.urls import patterns,  url

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

from stock import views

urlpatterns = patterns('',
                       url(r'^info=(?P<code>\w+)$',views.info,name='info'),
                       url(r'^choosed=(?P<userid>\w+)$',views.choosed,name='choosed'),
                       url(r'^stocks=(?P<userid>\w+)$',views.stocks,name='stocks'),
                       url(r'^watch=(?P<code>\w+)&userid=(?P<userid>\w+)$',views.watch,name='watch'),
                       url(r'^buy=(?P<code>\w+)&num=(?P<num>\w+)&price=(?P<price>\w+)&userid=(?P<userid>\w+)$',views.buy,name='buy'),
                       url(r'^sell=(?P<code>\w+)&num=(?P<num>\w+)&price=(?P<price>\w+)&userid=(?P<userid>\w+)$',views.sell,name='sell'))