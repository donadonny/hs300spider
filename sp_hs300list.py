#coding : utf-8

url_template = 'http://stock.finance.sina.com.cn/hs300/api/jsonp.json/\
SINAFINANCE141361734355447222/Cffex_PositionsService.getConditionHS300Data?page=%d'

import demjson,datetime 
from util import *

#table name
mongodb_collection = DB.hs300_list

def spider_hs300list():
    for i in range(1,10+1):
        url = url_template%i    
        content = http_spider(url)
        start = content.find('{')
        end = content.rfind('}')
        jsonStr = content[start:end+1]
        try:
            jsonObj = demjson.decode(jsonStr.decode('gbk'))
            n = len(jsonObj['data'])
            for j in range(n):
                data_object =  jsonObj['data'][j]
                data_object['stock_name'] = data_object['SYMBOL']
                data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
            
                update_condition = {"stock_name" : data_object['stock_name']}
                mongodb_update(mongodb_collection, update_condition, data_object)
        except ImportError, err:
            print err
            exit(0)
        print 'Spider: page %d  of 10 completed.' % i

if __name__ == "__main__":
    spider_hs300list()