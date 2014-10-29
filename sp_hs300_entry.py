#coding:utf-8
from util import *
import demjson,datetime,sys

import sp_hs300_day_summary as sp_summary
import sp_hs300_today_summary as sp_td_summary
import sp_hs300_day_detail as sp_detail
import sp_hs300_trade_day as sp_tradeday

def spider_trade_day(range):
    import sp_hs300_trade_day as sp
    print '------------------spider_trade_day------------------'
    sp.spider_trade_day(range=range)
    
def spider_hs300_list():
    import sp_hs300list as sp
    print '------------------spider_hs300_list------------------'
    sp.spider_hs300list()
    
def spider_hs300_summary(stock_name,date=None):
    print '------------------spider_hs300_summary------------------'
    if date:
        sp_summary.spider_day_summary(stock_name, date)
    else:
        sp_td_summary.spider_today_summary(stock_name)
    
def spider_hs300_detail(stock_name,date):
    print '------------------spider_hs300_detail------------------'
    sp_detail.spider_day_detail(stock_name, date) 

def spider_today():
    hs_300list = hs300_list()
    today = sp_td_summary.get_today()
    if not sp_tradeday.is_trade_day(today):
        print 'TODAY  %s is not tradeday.'%today
        exit(-1)
    
    for stock_name in hs_300list:        
        try:
            spider_hs300_summary(stock_name)
            spider_hs300_detail(stock_name, today)
        except Exception,err:
            print 'ERROR occured at date = ', today
            print 'ERR:', err
            print sys.exc_info()
            exit(-01)

#THE ENTRY POINT OF THE WHOLE SPIDER
def spider_entry(start_day, count):
    hs_300list = hs300_list()
    
    last_trade_days = hs300_last_trade_day(90)
    print 'last_trade_days = ',last_trade_days
    trade_day_set = set(last_trade_days)
    
    D = start_day
    N = count
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
    #spider_entry()
    spider_today()