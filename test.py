# -*- coding: utf-8 -*-

from util import *

'''
sort=[("date", AESC)]

r1 = read_db('hs300_day_summary',cond={'stock_name':'sh510050'},sort = sort)
r2 = read_db('hs300_day_summary',cond={'stock_name':'sh510900'},sort = sort)

def avp(item):
    return (item["open_price"]+ item["close_price"])/2


p1 = [avp(item) for item in r1]
p2 = [avp(item) for item in r2]

print len(p1), len(p2)

plt.figure()
plt.plot(p1)
plt.plot(p2)
plt.show()
'''


x = {'a':1, 'b': 2}
y = {'b':10, 'c': 11}
x.update(y)
print x,y