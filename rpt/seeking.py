# -*- coding: utf-8 -*-
"""
Created on Fri Mar 11 22:18:59 2016

@author: Xiaofeng
"""

#交易佣金
trade_fee = 0.002

class Seeking:
    def __init__(self):
        self.cash = 100000          #现金
        self.stock = 0              #股票
        self.idx = 0                #当前交易日
        self.price = 0              #当前价格，取avg(low,high)
        self.price_history=[]
    def handle(self, low, high):
        self.price_history.append((low,high))
        self.price = (low+high)/2.0
        self._action_()
        self.idx += 1
        return self.get_value()
    def _action_(self):
        pass
    '''以当日均价买入n手'''
    def buy(self, n):
        v = (n*100)*self.price*(1.0+trade_fee)
        assert(self.cash >= v)
        self.stock += n*100
        self.cash -= v
    '''以当日均价卖出n手'''    
    def sell(self, n):
        assert(self.stock >= n*100)
        self.stock -= n*100
        self.cash += (n*100)*self.price*(1.0-trade_fee)    
    def log(self):
        print 'Idx: %03d  Cash: %F  Stock: %F  Value: %F'%(self.idx,
                                                           self.cash,
                                                           self.stock*self.price,
                                                          self.get_value())
                
    def get_value(self):
        return self.cash + self.stock*self.price*(1-trade_fee)
        
        
class SimpleSeeking(Seeking):
    def __init__(self, cash_lv=1.0):
        Seeking.__init__(self)      #最大可用现金比例        
        self.cash_lv = cash_lv
    def _action_(self):
        Seeking._action_(self)
        if(self.idx==0):
            n = 0       #计算最大能买多少手
            while (n+1)*100*self.price*(1.0+trade_fee)<=(self.cash*self.cash_lv):
                n+=1
            self.buy(n)
        else:
            pass


class RebalanceSeeking(Seeking):
    def __init__(self, P = 2, Z = 0.15):
        Seeking.__init__(self)     
        self.P = P      #每隔P天一次再平衡
        self.Z = Z
    def _action_(self):
        Seeking._action_(self)
        if self.idx% self.P != 0:
            return
        stock_value = self.stock * self.price
        t = stock_value / self.cash
        if t<= 1+self.Z and t>=1-self.Z:
            return
        n = abs(stock_value - self.cash)/(self.price*100)
        n = int(n/2.0)
        print 'Before', t
        self.log()
        if t > 1:
            self.sell(n)
        else:
            self.buy(n)
        print 'After'
        self.log()
        