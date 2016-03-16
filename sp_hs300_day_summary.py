#coding:utf-8
from util import *
import demjson,datetime,db

db.connect()

#table name
mongodb_collection = DB.hs300_day_summary

#http://hq.sinajs.cn/rn=1414488384754&list=sh600188,rt_hk01171,RMBHKD,sh122168,bk_
url_template = 'http://vip.stock.finance.sina.com.cn/quotes_service/view/vMS_tradehistory.php?symbol=%s&date=%s'

sql_template = '''
insert into summary values(
	%d,	#ID
	'%s',#date
	%f,	#high_price
	%f,	#low_price
	%f,	#open_price
	%f,	#close_price
	%f,	#last_close_price
	%f,	#price_change
	%f,	#amount
	%f	#volume
);
'''

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
	v = float(v.replace('%',''))
        data_object[keys[i]] = v
     
    if data_object["open_price"] < 0.0001:
        print 'Invalid data, ignore @  %s, %s'%(stock_name,date)
        return
    
    sql = sql_template % (
        int(stock_name),
        date,
        data_object['high_price'],
        data_object['low_price'],
        data_object['open_price'],
        data_object['close_price'],
        data_object['last_close_price'],
        data_object['price_change'],
        data_object['amount'],
        data_object['volume']
    )
    db.exeSQL(sql)

def spider_day_summary(stock_name,date):
    print '-- spider_day_summary : stock_name=%s, date=%s'%(stock_name,date)
    url = url_template%('sh'+stock_name,date)
    data = http_spider(url)
    data = data.decode('gbk').encode('utf-8')
    try:
        handle_day_summary_data(stock_name, date, data)
    except Exception,err:
        print 'spider_day_summary ERROR! @ %s,  %s' %(stock_name,date)
        #print 'URL = %s' % url
        print 'ERROR :', err
        #raise err

if __name__ == "__main__":
    ds = hs300_last_trade_day(count = 600)
    stocks = ['510050','510900']
    for d in ds:
        for s in stocks:
            spider_day_summary(s,d)
