#coding:utf-8
from util import *
import demjson,datetime,sys

import sp_hs300_day_summary as sp_summary
import sp_hs300_day_detail as sp_detail

def spider_trade_day(range):
    import sp_hs300_trade_day as sp
    print '------------------spider_trade_day------------------'
    sp.spider_trade_day(range=range)
    
def spider_hs300_list():
    import sp_hs300list as sp
    print '------------------spider_hs300_list------------------'
    sp.spider_hs300list()
    
def spider_hs300_summary(stock_name,date):
    print '------------------spider_hs300_summary------------------'
    sp_summary.spider_day_summary(stock_name, date)
    
def spider_hs300_detail(stock_name,date):
    print '------------------spider_hs300_detail------------------'
    sp_detail.spider_day_detail(stock_name, date) 

#THE ENTRY POINT OF THE WHOLE SPIDER
def spider_entry():
    #spider_trade_day(range=90)
    #spider_hs300_list()
    
    hs_300list = hs300_list()
    last_trade_days = hs300_last_trade_day(count=90)
    print 'last_trade_days = ',last_trade_days
    
    trade_day_set = set(last_trade_days)
    D = datetime.date(2014,8,13)
    N = 30
    oneday = datetime.timedelta(days=1)
    for i in range(N):
        D -= oneday
        date = D.strftime(DT_FMT_SHORT)
        print '-- DATE = ', date
        if not date in trade_day_set:
            continue
        
        for stock_name in hs_300list:        
            try:
                spider_hs300_summary(stock_name,date)
                spider_hs300_detail(stock_name, date)
            except Exception,err:
                print 'ERROR occured at date = ', date
                print 'ERR:', err
                print sys.exc_info()
                exit(-01)
    print '-----------ALL COMPLETE-----------'
    print 'LAST date:',date

if __name__ == "__main__":
    spider_entry()