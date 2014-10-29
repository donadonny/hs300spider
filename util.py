# coding : utf-8

import urllib2,time
from pymongo import MongoClient,DESCENDING,ASCENDING 

DBClient = MongoClient('mongodb://localhost:27017/')
DB = DBClient.hs300
DT_FMT = '%Y-%m-%d %H:%M:%S %Z'
DT_FMT_SHORT = '%Y-%m-%d'
def http_spider(url,retry_count=5):
    def http_request():
        print 'Spider URL:',url
        fd = urllib2.urlopen(url)
            
        content = ''
        while True:
            d = fd.read()
            if d: content+=d
            else:break
        return content
    t = 0.01
    while True:
        try:
            return http_request()
        except Exception,err:
            retry_count -= 1
            if retry_count==0:
                raise err
            time.sleep(t)
            t*=2


def mongodb_update(mongodb_collection, update_condition, data_object,debug=False):
    res = mongodb_collection.find_one(update_condition)
    if res:
        data_object['_id'] = res['_id']
        mongodb_collection.save(data_object)
        if debug:
            print 'UPDATE ID = ', res['_id']
    else:
        id = mongodb_collection.insert(data_object)
        if debug:
            print 'Insert ID = ', id
    pass


def html_extract(html,keyTag,position=0):
    #print 'html_extract : ',keyTag,position
    p1 = html.find(keyTag,position)
    m=True
    while True:
        ch = html[p1]
        if ch=='>':m=False
        elif ch=='<':m=True
        elif ch==' ' or ch=='\t' or ch=='\n':pass
        else:
            if m==False:
                break
            else:pass
        p1 += 1
        if p1>=len(html):
            p1=-1
            break
    #print p1
    if p1==-1:return (None,None)
    p2 = html.find('<',p1)
    if p2==-1:return (None,None)
    #print p1,p2
    #print html[p1-3:p1+3]
    #print html[p1:p2],p2
    return (html[p1:p2],p2)
    

def hs300_list():
    mongodb_collection = DB.hs300_list
    records = mongodb_collection.find().sort([("_update_time_", DESCENDING)])
    return [records[i]['stock_name']for i in range(300)]

def hs300_last_trade_day(count=10):
    mongodb_collection = DB.hs300_trade_day
    records = mongodb_collection.find().sort([("date", DESCENDING)])
    return [records[i]['date']for i in range(count)]

def day_range(year,month,day,range):
    pass
        
if __name__ == "__main__":
    #print hs300_list()
    print hs300_last_trade_day(30)