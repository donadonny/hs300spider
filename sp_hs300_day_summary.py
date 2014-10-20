#coding:utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_day_summary

url_template = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=%s&date=%s'

tags=['收盘价:<','涨跌幅:<','前收价:<','开盘价:<','最高价:<','最低价:<','成交量(手):<','成交额(千元):<']
keys=['close_price','price_change','last_close_price','open_price','high_price','low_price','amount','volume']

def handle_day_summary_data(stock_name,date,html):    
    data_object = dict()
    data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
    data_object['stock_name'] = stock_name
    data_object['date'] = date
    
    
    #lambda_fun = [float,float,float,float,float,float,int,int]
    tag_count = len(tags)
    assert(tag_count==len(keys))
    
    p=0
    for i in range(0,tag_count):
        (v,p) = html_extract(html, tags[i],position=p)
        #print v,p
        assert(v)
        data_object[keys[i]] = float(v.replace('%',''))
        
    update_condition = {"stock_name":data_object['stock_name'],
                            'date':data_object['date']}
    #update !
    print data_object
    mongodb_update(mongodb_collection, update_condition, data_object)

def spider_day_summary(stock_name,date):
    print '-- spider_day_summary : stock_name=%s, date=%s'%(stock_name,date)
    url = url_template%(stock_name,date)
    data = http_spider(url)
    data = data.decode('gbk').encode('utf-8')
    try:
        handle_day_summary_data(stock_name, date, data)
    except Exception,err:
        print 'spider_day_summary ERROR!'
        print 'URL = %s' % url
        raise err

if __name__ == "__main__":
    data = spider_day_summary('sh600188', '2014-06-18')