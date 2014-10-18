# coding : utf-8

import urllib2
from pymongo import MongoClient

DBClient = MongoClient('mongodb://localhost:27017/')
DB = DBClient.hs300
DT_FMT = '%Y-%m-%d %H:%M:%S %Z'

def http_spider(url):
    print 'Spider URL:',url
    fd = urllib2.urlopen(url)
        
    content = ''
    while True:
        d = fd.read()
        if d: content+=d
        else:break
    return content   


def mongodb_update(mongodb_collection, update_condition, data_object):
    res = mongodb_collection.find_one(update_condition)
    if res:
        data_object['_id'] = res['_id']
        mongodb_collection.save(data_object)
    else:
        mongodb_collection.insert(data_object)
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
    

if __name__ == "__main__":
    print '->',html_extract('<tr><td>xx:</td><td>6.64</td></tr>', 'xx:</td><td>')