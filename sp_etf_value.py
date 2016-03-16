# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 16:34:11 2016

@author: xiaofeng
"""

from util import *
import demjson,datetime,decimal

#table name
mongodb_collection = DB.hs300_day_summary

url_template = 'http://www.jjmmw.com/fund/ajax/get_fund_his_nav/?fundcode=%s&beginDate=%s&endDate=%s'

sql_template = '''
replace into etf_nv values(
	%d,    #ID
	'%s',  #date
	%f,	#accum_net
	%f,	#unit_net
	%f,	#unit_net_chng_pct
	'%s'	#growth_rate
);'''

import db
db.connect()

def handle_day_detail_data(stock_name,data):
    pyObj = demjson.decode(data)['his_nav_list']
    
    n = len(pyObj)
    print '\tGot %d records.'%n
    for r in pyObj:
        for k,v in r.items():
            if type(v) == type(decimal.Decimal(1.0)):
                r[k] = float(v)
        sql = sql_template %(
            int(stock_name),
            r["tradedate_display2"],
            r["accum_net"],
            r["unit_net"],
            r["unit_net_chng_pct"],
            r["growth_rate"]
        )
        print sql
        db.exeSQL(sql)
        
    
        
def spider_day_detail(stock_name,beigin_date,end_date):
    url = url_template%(stock_name,beigin_date,end_date)
    data = http_spider(url)
    try:
        handle_day_detail_data(stock_name, data)
    except Exception, err:
        print 'spider_day_detail ERROR!'
        print 'URL = %s' % url
        print 'ERROR :', err
        raise err

if __name__ == "__main__":
    ds = hs300_last_trade_day(count = 600 + 1)
    stocks = ['510050','510900']
    for i in range(len(ds)-1):
        for s in stocks:
            spider_day_detail(s,ds[i],ds[i+1])
        #break