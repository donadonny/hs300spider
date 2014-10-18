# coding : utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_day_summary

url_template = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=%s&date=%s'

def spider_day_detail(stock_name,date):
    url = url_template%(stock_name,date)
    data = http_spider(url)
    return data.decode('gbk').encode('utf-8')

def handle_day_detail_data(stock_name,date,html):    
    data_object = dict()
    data_object['stock_name'] = stock_name
    data_object['date'] = date
    
    tags=['收盘价:<',
          '涨跌幅:<',
          '前收价:<',
          '开盘价:<',
          '最高价:<',
          '最低价:<',
          '成交量(手):<',
          '成交额(千元):<']
    keys=['close_price','price_change','last_close_price','open_price','high_price','low_price','amount','volume']
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
    mongodb_update(mongodb_collection, update_condition, data_object)   

if __name__ == "__main__":
    data = spider_day_detail('sh600188', '2014-06-18')
    #print data
    handle_day_detail_data('sh600188', '2014-06-18',data)