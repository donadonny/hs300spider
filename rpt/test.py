# -*- coding: utf-8 -*-
"""
Created on Thu Mar 10 23:07:46 2016

@author: Xiaofeng
"""
import urllib2,time
from pymongo import MongoClient,DESCENDING,ASCENDING 

DBClient = MongoClient('mongodb://localhost:27017/')
db = DBClient.hs300.hs300_day_summary

ds = db.find().sort([("date", ASCENDING)])


price = []

for i in ds:
    if i["low_price"] < 1:
        continue
    price.append((i["low_price"],i["high_price"]))


price = price[140:270]   

'''
price = [(1,1)]
for i in range(2):
    price.append((2,2))
    price.append((1,1))
'''
DN = len(price)
x = range(DN)
 



from seeking import SimpleSeeking,RebalanceSeeking

seekers = [
    SimpleSeeking(cash_lv=1.0),
    SimpleSeeking(cash_lv=.5),
    RebalanceSeeking(P=1,Z=0.02)
]

for i in range(10):
    seekers.append(RebalanceSeeking(P=i+2,Z=0.05))

values = [[] for i in seekers]


for i in range(DN):
    for j in range(len(seekers)):
        seeker,value = seekers[j],values[j]
        value.append(seeker.handle(price[i][0],price[i][1]))
    
import matplotlib.pyplot as plt

plt.subplot(211)  
plt.plot(x,[a for (a,b) in price])
plt.plot(x,[b for (a,b) in price])
plt.plot(x,[sum(price[0])/2 for i in range(DN)])

plt.subplot(212)

for j in range(len(seekers)):
    value = values[j]
    plt.plot(x,value)
plt.plot(x,[100000 for i in range(DN)])
plt.show()  

for j in range(len(seekers)):
    print seekers[j].get_value()