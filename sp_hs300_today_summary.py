#coding:utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_day_summary


url_template = 'http://hq.sinajs.cn/list=%s'

#price_change = (close_price-last_close_price)/last_close_price
tags=[3,-1,2,1,4,5,8,9]
keys=['close_price','price_change','last_close_price','open_price','high_price','low_price','amount','volume']

def get_today():
    return datetime.datetime.now().strftime(DT_FMT_SHORT)
    
def handle_today_summary_data(stock_name,date,html): 
    a = html.find('"')
    b = html.rfind('"')
    html = html[a:b]
    
    values = html.split(',')
    
    data_object = dict()
    data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
    data_object['stock_name'] = stock_name
    data_object['date'] = date
    
    for i in range(len(tags)):
        idx = tags[i]
        key = keys[i]
        if idx <0:continue
        data_object[key] = float(values[idx])
    
    data_object['price_change'] = (data_object['close_price']-data_object['last_close_price'])*100/data_object['last_close_price']
    data_object['volume'] /= 1000.0
    data_object['amount'] /= 100.0
    update_condition = {"stock_name":data_object['stock_name'],
                            'date':data_object['date']}
    #update !
    #print data_object
    mongodb_update(mongodb_collection, update_condition, data_object)

def spider_today_summary(stock_name):
    date = get_today()
    print '-- spider_day_summary : stock_name=%s, date=%s'%(stock_name,date)
    url = url_template%(stock_name)
    data = http_spider(url)
    data = data.decode('gbk').encode('utf-8')
    try:
        handle_today_summary_data(stock_name, date, data)
    except Exception,err:
        print 'spider_day_summary ERROR!'
        print 'URL = %s' % url
        print 'ERROR :', err
        raise err

if __name__ == "__main__":
    data = spider_today_summary('sh600188')