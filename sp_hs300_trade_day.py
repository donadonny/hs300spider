#coding : utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_trade_day

url_template = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=sh600188'


def update_mongodb(date):
    data_object = dict()
    data_object['date'] = date
    data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
    update_condition = {'date':data_object['date']}
    #update !
    mongodb_update(mongodb_collection, update_condition, data_object)      
    
def spider_trade_day(range=30):
    today = datetime.datetime.now()
    n = 0
    while n < range:
        oneday = datetime.timedelta(days=1)
        today -= oneday
        date = today.strftime(DT_FMT_SHORT)
        url = url_template%date
        data = http_spider(url)
        if len(data) <= 1200:#not a trade day
            pass
        else:#is trade day
            n+=1
            update_mongodb(date)

if __name__ == "__main__":
    spider_trade_day()