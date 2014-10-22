#coding : utf-8
import sys
sys.path.append("../")
from util import *
import datetime


mongodb_coll_summary = DB.hs300_day_summary
mongodb_coll_details = DB.hs300_day_detail

def bool2int(b):
    if b:return 1
    else:return -1

def generate_oneday_feature(day_index,date,stock_name):
    query = {"stock_name":stock_name,'date':date}
    res = mongodb_coll_summary.find_one(query)
    if not res:return None
    f = [res["high_price"],
         res["low_price"],
         res["price_change"],
         
         #res["last_close_price"],
         res["open_price"],
         res["close_price"],
         bool2int(res["close_price"]>res["open_price"]),
         bool2int(res["open_price"]>res["last_close_price"]),
         res["high_price"]-res["low_price"],
         res["low_price"]-res["close_price"],
         res["high_price"]-res["open_price"],
         int(res["volume"]/10000),
         int(res["amount"]/10000)]
    return f

def generate_feature(stock_name,x_days):
    feature = []
    for i in range(len(x_days)):
        f = generate_oneday_feature(i,x_days[i],stock_name)
        if not f:
            print '--> Cannot generate_feature for stock : %s , at trade day :%s' %(stock_name,x_days[i])
            return None
        feature += f
    return feature

if __name__ == "__main__":
    print generate_feature('sh601989', ['2014-07-18'])
