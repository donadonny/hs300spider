# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 17:46:20 2016

@author: xiaofeng
"""

import MySQLdb


conn = None

def connect():
    global conn
    conn = MySQLdb.connect(host='localhost',user='root',passwd='111111',port=3306)
    conn.select_db('hs300')
    pass
 
 

def exeSQL(sql):
    if not conn:raise BaseException('Connect DB First')
    cur=conn.cursor()
    cur.execute(sql)
    conn.commit()
    cur.close()
    
def fetch(querySQL):
    if not conn:raise BaseException('Connect DB First')
    cur =  conn.cursor()
    count=cur.execute(querySQL)
    print 'there has %s rows record' % count
    return cur.fetchall()


if __name__ == "__main__":
    #connect()
    print fetch('select * from test')