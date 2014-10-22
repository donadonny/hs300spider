#coding : utf-8
import sys
sys.path.append("../")
from util import *
import datetime

mongodb_collection = DB.hs300_day_summary

def generate_ylabel(stock_name,yday):
    query = {"stock_name":stock_name,'date':yday}
    res = mongodb_collection.find_one(query)
    if not res:return None
    if not res.has_key("price_change"):return None
    return res["price_change"]

if __name__ == "__main__":
    D = datetime.date(2014,6,9)
    D = D.strftime(DT_FMT_SHORT)
    print generate_ylabel('sz000401',D)
