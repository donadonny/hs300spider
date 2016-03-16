# coding : utf-8

import urllib2,time
from pymongo import MongoClient,DESCENDING,ASCENDING 

DBClient = MongoClient('mongodb://localhost:27017/')
DB = DBClient.hs300
DT_FMT = '%Y-%m-%d %H:%M:%S %Z'
DT_FMT_SHORT = '%Y-%m-%d'

DESC = DESCENDING
AESC = ASCENDING
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
        #data_object['_id'] = res['_id']
        data_object.update(res)
        mongodb_collection.save(data_object)
        print res
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
    


    

def read_db(table,cond = None,sort = None):
    mongodb_collection = getattr(DB,table)
    records = mongodb_collection.find(cond)
    if sort:
        records = records.sort(sort)
    return records

def hs300_list():
    records = read_db("hs300_list",None,[("stock_name", DESC)])
    return [records[i]['stock_name']for i in range(300)]
    
def hs300_last_trade_day(count=10):
    import datetime
    now = datetime.datetime.now()
    oneday = datetime.timedelta(days = 1)
    ds=[]
    while len(ds)<count:
        idx = int(now.strftime("%u"))
        if idx>=1 and idx<=5:
            ds.append(now.strftime("%Y-%m-%d"))
        now -= oneday
    ds.sort()
    return ds
    

    
if __name__ == "__main__":
    print hs300_last_trade_day()