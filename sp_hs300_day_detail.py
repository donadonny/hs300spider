#coding : utf-8
from util import *
import demjson,datetime 

#table name
mongodb_collection = DB.hs300_day_detail

url_template = 'http://market.finance.sina.com.cn/downxls.php?date=%s&symbol=%s'

def spider_day_detail(stock_name,date):
    url = url_template%(date,stock_name)
    data = http_spider(url)
    return data.decode('gbk')

def handle_day_detail_data(stock_name,date,data):
    lines = data.split('\n')
    assert(len(lines)>=1)
    header = lines[0].split('\t')
    n = len(header)
    for x in header:
        print 'Header : '+x
    
    line_count = len(lines)-1
    for i in range(1,len(lines)):
        if i%50==0:
            print '-- %d of %d lines completed.'%(i,line_count)
        line = lines[i]
        cells = line.split('\t')
        if len(cells)!=6:
            print 'Warning! Cannot handle text line:', line
            continue
        data_object = dict()
        
        data_object['stock_name'] = stock_name
        data_object['date'] = date
        data_object['time'] = cells[0]
        data_object['price'] = float(cells[1])
        data_object['price_delta'] = float(cells[2].replace('--','0'))
        data_object['amount'] = int(cells[3])
        data_object['volume'] = int(cells[4])
        data_object['property'] = cells[5]
        
        data_object['_update_time_'] = datetime.datetime.now().strftime(DT_FMT)
        update_condition = {"stock_name":data_object['stock_name'],
                            'date':data_object['date'],
                            'time':data_object['time']}
        #update !
        mongodb_update(mongodb_collection, update_condition, data_object)        
        

if __name__ == "__main__":
    data = spider_day_detail('sh600188', '2014-06-18')
    handle_day_detail_data('sh600188', '2014-06-18',data)