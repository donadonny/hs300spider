#coding : utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_trade_day

url_template = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=sh600188'
url_template2 = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=sh601398'


def update_mongodb(date):
    data_object = dict()
    data_object['date'] = date
    data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
    update_condition = {'date':data_object['date']}
    #update !
    mongodb_update(mongodb_collection, update_condition, data_object)      
    
def is_trade_day(date):
    data = http_spider(url_template%date)
    data2 = http_spider(url_template2%date)
    return len(data)>=1200 or len(data2)>=1200

<<<<<<< HEAD
def spider_trade_day(range=360):
=======
def spider_trade_day(range=300):
>>>>>>> 676a11505ee8be241cd3a4f0fecb92980958079f
    today = datetime.datetime.now()
    oneday = datetime.timedelta(days=1)
    today += oneday
    n = 0
    while n < range:
        today -= oneday
        date = today.strftime(DT_FMT_SHORT)
        
        if not is_trade_day(date):
            pass
        else:#is trade day
            n+=1
            update_mongodb(date)

if __name__ == "__main__":
    spider_trade_day()
